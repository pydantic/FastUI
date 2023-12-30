import typing as _t

import pydantic

from .components import AnyComponent

__version__ = '0.4.0'
__all__ = 'AnyComponent', 'FastUI', 'prebuilt_html'


class FastUI(pydantic.RootModel):
    """
    The root component of a FastUI application.
    """

    root: _t.List[AnyComponent]

    @pydantic.field_validator('root', mode='before')
    def coerce_to_list(cls, v):
        if isinstance(v, list):
            return v
        else:
            return [v]


_PREBUILT_VERSION = '0.0.15'
_PREBUILT_CDN_URL = f'https://cdn.jsdelivr.net/npm/@pydantic/fastui-prebuilt@{_PREBUILT_VERSION}/dist/assets'


def prebuilt_html(title: str = ''):
    """
    Returns a simple HTML page which includes the FastUI react frontend, loaded from https://www.jsdelivr.com/.

    Arguments:
        title: page title

    Returns:
        HTML string which can be returned by an endpoint to serve the FastUI frontend.
    """
    # language=HTML
    return f"""\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <script type="module" crossorigin src="{_PREBUILT_CDN_URL}/index.js"></script>
    <link rel="stylesheet" crossorigin href="{_PREBUILT_CDN_URL}/index.css">
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
"""
