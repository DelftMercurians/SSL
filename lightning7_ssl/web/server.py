import asyncio
import atexit
import json
import os
import subprocess
import time
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from ..vis.data_store import DataStore

SERVER_PORT = 5000
dist_folder = Path(__file__).parent / "frontend" / "dist"


def run_server(pipe: Connection, ui_dev_server=False):
    """Run a web server to serve the visualization."""
    import uvicorn
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import BaseRoute, Mount, Route
    from starlette.staticfiles import StaticFiles

    state: Dict = {}

    async def get_state(request):
        return JSONResponse(state)

    async def pipe_reader():
        loop = asyncio.get_event_loop()
        while True:
            try:
                data = await loop.run_in_executor(None, pipe.recv)
            except KeyboardInterrupt:
                return
            if isinstance(data, str):
                state.update(json.loads(data))
            elif isinstance(data, dict):
                state.update(data)

    async def run_server() -> None:
        routes: List[BaseRoute] = [
            Route("/api/state", get_state),
        ]
        if not ui_dev_server:
            routes.append(
                Mount(
                    "/",
                    app=StaticFiles(directory=dist_folder, html=True),
                    name="static",
                )
            )
        app = Starlette(
            debug=True,
            routes=routes,
        )
        config = uvicorn.Config(app, port=SERVER_PORT, log_level="critical")
        server = uvicorn.Server(config)
        print("Serving from " + str(dist_folder))
        try:
            await server.serve()
        except KeyboardInterrupt:
            print("Shutting down server")
            await server.shutdown()

    async def main():
        await asyncio.gather(run_server(), pipe_reader())

    asyncio.run(main())


class ServerWrapper:
    _process: Optional[Process] = None
    _dev_process: Optional[subprocess.Popen] = None

    def __init__(self, open_browser=False, ui_dev_server=False) -> None:
        if ui_dev_server:
            env = dict(os.environ, PROXY_PORT=str(SERVER_PORT))
            if open_browser:
                env["OPEN_BROWSER"] = "1"
            self._dev_process = subprocess.Popen(
                ["npm", "run", "dev", "--", "-l", "error"],
                cwd=dist_folder.parent,
                env=env,
                stdin=subprocess.DEVNULL,
            )
            time.sleep(1)
        self._pipe, child_pipe = Pipe()
        self._process = Process(target=run_server, args=(child_pipe, ui_dev_server), daemon=True)
        self._process.start()
        atexit.register(self.stop)

    def stop(self):
        if self._process is not None and self._process.is_alive():
            self._process.terminate()
            print("Stopping web server... (this may take a few seconds)")
            self._process.join(1)
            if self._process.is_alive():
                self._process.kill()
            self._process = None
        if self._dev_process is not None and self._dev_process.poll() is None:
            self._dev_process.terminate()
            print("Stopping dev server... (this may take a few seconds)")
            self._dev_process.wait(1)
            if self._dev_process.poll() is None:
                self._dev_process.kill()
            self._dev_process = None

    def recv(self):
        """Non-blocking receive from the server."""
        if self._process is None or not self._process.is_alive():
            raise RuntimeError("Server is not running")
        if self._pipe.poll():
            return self._pipe.recv()
        return None

    def send(self, data):
        if self._process is None or not self._process.is_alive():
            raise RuntimeError("Server is not running")
        self._pipe.send(data)

    def step(self, _, ds: "DataStore") -> None:
        self.send(ds.to_json())

    def __del__(self):
        self.stop()
