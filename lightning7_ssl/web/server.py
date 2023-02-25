import asyncio
import json
from multiprocessing.connection import Connection
from pathlib import Path

dist_folder = Path(__file__).parent / "frontend" / "dist"


def run_server(pipe: Connection):
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
            data = await loop.run_in_executor(None, pipe.recv)
            if isinstance(data, str):
                state.update(json.loads(data))
            elif isinstance(data, dict):
                state.update(data)

    async def run_server():
        app = Starlette(
            debug=True,
            routes=[
                Route("/api/state", get_state),
                Mount("/", app=StaticFiles(directory=dist_folder), name="static"),
            ],
        )
        config = uvicorn.Config(app, port=5000, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

    asyncio.run(asyncio.gather(run_server(), pipe_reader()))
