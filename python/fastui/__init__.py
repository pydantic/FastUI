__version__ = '0.0.1'

import pydantic

from .components import AnyComponent
from .dev import dev_fastapi_app
from .display import Display

__all__ = 'AnyComponent', 'FastUI', 'dev_fastapi_app', 'Display'


class FastUI(pydantic.RootModel):
    root: AnyComponent
