__version__ = '0.0.1'

from pydantic import RootModel

from .components import AnyComponent


class FastUI(RootModel):
    root: AnyComponent
