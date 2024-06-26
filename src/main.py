import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.tg.router import tg_router
from src.integrations.tg_bot import bot
from src.middleware.logger import LogServerMiddleware
from src.middleware.metrics import MetricsMiddleware, metrics
from src.on_startup.logger import setup_logger
from src.on_startup.webhook import setup_webhook
from src.utils.background_tasks import tg_background_tasks


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(LogServerMiddleware)
    app.add_middleware(MetricsMiddleware)
    # CORS Middleware should be the last.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],  # type: ignore
        allow_credentials=True,  # type: ignore
        allow_methods=['*'],  # type: ignore
        allow_headers=['*'],  # type: ignore
    )


def setup_routers(app: FastAPI) -> None:
    app.add_route('/metrics', metrics)
    app.include_router(tg_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print('START APP')
    await setup_webhook(bot)
    setup_logger()

    yield

    logging.info('Stopping')

    while len(tg_background_tasks) > 0:
        logging.info('%s tasks left', len(tg_background_tasks))
        await asyncio.sleep(0)

    logging.info('Stopped')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)

    setup_middleware(app)
    setup_routers(app)

    return app
