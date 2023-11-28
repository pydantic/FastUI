__version__ = '0.0.1'

import pydantic

from .components import AnyComponent
from .dev import dev_fastapi_app

__all__ = 'AnyComponent', 'FastUI', 'dev_fastapi_app'


class FastUI(pydantic.RootModel):
    root: list[AnyComponent]
