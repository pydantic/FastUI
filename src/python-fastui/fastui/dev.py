import asyncio
import os
import signal
import typing as _t
from contextlib import asynccontextmanager

try:
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse
    from starlette import types
except ImportError as e:
    raise ImportError('fastui.dev requires fastapi to be installed, install with `pip install fastui[fastapi]`') from e


def dev_fastapi_app(reload_path: str = '/api/__dev__/reload', **fastapi_kwargs) -> FastAPI:
    dev_reload = DevReload(fastapi_kwargs.pop('lifespan', None))

    app = FastAPI(lifespan=dev_reload.lifespan)
    app.get(reload_path, include_in_schema=False)(dev_reload.dev_reload_endpoints)
    return app


class DevReload:
    def __init__(self, default_lifespan: _t.Union[types.Lifespan[FastAPI], None]):
        self.default_lifespan = default_lifespan
        self.stop = asyncio.Event()

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        signal.signal(signal.SIGTERM, self._on_signal)
        if self.default_lifespan:
            async with self.default_lifespan(app):
                yield
        else:
            yield

    async def dev_reload_endpoints(self):
        return StreamingResponse(self.ping(), media_type='text/plain')

    def _on_signal(self, *_args: _t.Any):
        # print('setting stop', _args)
        self.stop.set()

    async def ping(self):
        # print('connected', os.getpid())
        yield b'fastui-dev-reload\n'
        yield b'.'
        while True:
            try:
                await asyncio.wait_for(self.stop.wait(), timeout=2)
            except asyncio.TimeoutError:
                yield b'.'
            else:
                yield b'%d' % os.getpid()
                break
