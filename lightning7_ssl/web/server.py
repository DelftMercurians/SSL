import asyncio
from pathlib import Path

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute, Mount, Route
from starlette.staticfiles import StaticFiles

from lightning7_ssl.utils.rpc import AsyncService, expose

SERVER_PORT = 5000
dist_folder = Path(__file__).parent / "frontend" / "dist"


class WebService(AsyncService):
    state: dict | None = None

    def __init__(
        self,
        open_browser=False,
        ui_dev_server=False,
        ui_host: str | None = None,
        ui_port: int | None = None,
    ) -> None:
        self.open_browser = open_browser
        self.ui_dev_server = ui_dev_server
        self.ui_host = ui_host
        self.ui_port = ui_port
        self.server_task = asyncio.create_task(self.run_server())

    @expose
    def set_state(self, state: dict):
        self.state = state

    async def get_state(
        self,
    ):
        if self.state is None:
            return JSONResponse(None, status_code=404)
        return JSONResponse(self.state)

    async def run_server(self) -> None:
        routes: list[BaseRoute] = [
            Route("/api/state", self.get_state),
        ]
        if not self.ui_dev_server:
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
        except (KeyboardInterrupt, asyncio.CancelledError):
            print("Shutting down server")
            await server.shutdown()
