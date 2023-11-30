import pydantic

from .components import AnyComponent

__version__ = '0.2.0'
__all__ = 'AnyComponent', 'FastUI', 'prebuilt_html'


class FastUI(pydantic.RootModel):
    root: list[AnyComponent]


_PREBUILT_VERSION = '0.0.6'
_PREBUILT_CDN_URL = f'https://cdn.jsdelivr.net/npm/@pydantic/fastui-prebuilt@{_PREBUILT_VERSION}/dist/assets'


def prebuilt_html(title: str = ''):
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
