__version__ = '0.0.1'

import pydantic

from .components import AnyComponent

__all__ = 'AnyComponent', 'FastUI'


class FastUI(pydantic.RootModel):
    root: AnyComponent
