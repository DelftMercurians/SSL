import asyncio
import atexit
import json
import subprocess
from multiprocessing.connection import Connection
from multiprocessing import Pipe, Process
import os
from pathlib import Path
import time
from typing import TYPE_CHECKING, Optional
import webbrowser

if TYPE_CHECKING:
    from ..vis.data_store import DataStore

SERVER_PORT = 5000
dist_folder = Path(__file__).parent / "frontend" / "dist"


def run_server(pipe: Connection, dev_mode=False):
    """Run a web server to serve the visualization."""
    import uvicorn
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Mount, Route
    from starlette.staticfiles import StaticFiles

    state = {}

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

    async def run_server():
        routes = [
            Route("/api/state", get_state),
        ]
        if not dev_mode:
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

    def __init__(self, force_dev_mode=False):
        dev_mode = force_dev_mode or bool(os.environ.get("DEV_MODE", False))
        if dev_mode:
            self._dev_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=dist_folder.parent,
                env=dict(os.environ, PROXY_PORT=str(SERVER_PORT)),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(1)
        self._pipe, child_pipe = Pipe()
        self._process = Process(
            target=run_server, args=(child_pipe, dev_mode), daemon=True
        )
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

    def send(self, data):
        if self._process is None or not self._process.is_alive():
            raise RuntimeError("Server is not running")
        self._pipe.send(data)

    def step(self, _, ds: "DataStore") -> None:
        self.send(ds.to_json())

    def __del__(self):
        self.stop()
