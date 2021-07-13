from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import config, task
from app.api.routes import router as api_router


def get_application():
    """get_application

        applicationの各種設定

    """
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", task.create_start_app_handler(app))
    app.add_event_handler("shutdown", task.create_stop_app_handler(app))

    app.include_router(api_router, prefix="/api/v1")

    return app


app = get_application()
