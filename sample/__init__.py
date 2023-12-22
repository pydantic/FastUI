from __future__ import annotations as _annotations

import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastui import prebuilt_html
from fastui.dev import dev_fastapi_app
from httpx import AsyncClient

# from .app import create_db


# @asynccontextmanager
# async def lifespan(app_: FastAPI):
#     await create_db()
#     async with AsyncClient() as client:
#         app_.state.httpx_client = client
#         yield


frontend_reload = '--reload' in sys.argv
if frontend_reload:
    # dev_fastapi_app reloads in the browser when the Python source changes
    app = dev_fastapi_app()
else:
    app = FastAPI()


@app.get('/robots.txt', response_class=PlainTextResponse)
async def robots_txt() -> str:
    return 'User-agent: *\nAllow: /'


@app.get('/favicon.ico', status_code=404, response_class=PlainTextResponse)
async def favicon_ico() -> str:
    return 'page not found'


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))
