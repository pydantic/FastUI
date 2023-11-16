__version__ = '0.0.1'

import pydantic

from .components import AnyComponent
from .form_extract import FormResponse, fastui_form

__all__ = 'FastUI', 'fastui_form', 'FormResponse', 'AnyComponent'


class FastUI(pydantic.RootModel):
    root: AnyComponent
