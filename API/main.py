import asyncio
import logging
import os.path
from contextlib import asynccontextmanager

import fastapi_cli.cli
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware

from core.storages import Database
from services.slides import routes


@asynccontextmanager
async def lifespan(instance: FastAPI):
    if not os.path.isdir("files"):
        os.mkdir("files")
    for i in range(3):
        try:
            await Database.init()
            break
        except Exception as e:
            logging.error(e)
            logging.warning("попытка повторного подключения к базе")
            if i == 2: raise Exception("подключение к базе не удалось", e)
            await asyncio.sleep(5 ** i)
    yield


app = FastAPI(lifespan=lifespan,
              docs_url=None,
              redoc_url=None,
              root_path="/api", )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


# @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
# async def swagger_ui_redirect():
#     return get_swagger_ui_oauth2_redirect_html()


app.include_router(routes.router)

if __name__ == '__main__':
    fastapi_cli.cli.run()
