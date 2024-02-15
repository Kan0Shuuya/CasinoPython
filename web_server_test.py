from aiohttp import web
from loguru import logger

logger.debug("Initializing web server structures...")

async def handle(request) -> web.Response:
    logger.debug("Request received")
    return web.Response(text="Hello, world")

webApp = web.Application()
webApp.router.add_get('/', handle)

def start_server(port: int) -> None:
    logger.info(f"Starting web server on port {port}")
    web.run_app(webApp, port=port)