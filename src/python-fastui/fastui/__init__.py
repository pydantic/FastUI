import typing as _t

import pydantic

from .components import AnyComponent

__version__ = '0.5.2'
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


_PREBUILT_VERSION = '0.0.22'
_PREBUILT_CDN_URL = f'https://cdn.jsdelivr.net/npm/@pydantic/fastui-prebuilt@{_PREBUILT_VERSION}/dist/assets'


def prebuilt_html(
    *,
    title: str = '',
    api_root_url: _t.Union[str, None] = None,
    api_path_mode: _t.Union[_t.Literal['append', 'query'], None] = None,
    api_path_strip: _t.Union[str, None] = None,
) -> str:
    """
    Returns a simple HTML page which includes the FastUI react frontend, loaded from https://www.jsdelivr.com/.

    Arguments:
        title: page title
        api_root_url: the root URL of the API backend, which will be used to get data, default is '/api'.
        api_path_mode: whether to append the page path to the root API request URL, or use it as a query parameter,
            default is 'append'.
        api_path_strip: string to remove from the start of the page path before making the API request.

    Returns:
        HTML string which can be returned by an endpoint to serve the FastUI frontend.
    """
    meta_extra = []
    if api_root_url is not None:
        meta_extra.append(f'<meta name="fastui:APIRootUrl" content="{api_root_url}" />')
    if api_path_mode is not None:
        meta_extra.append(f'<meta name="fastui:APIPathMode" content="{api_path_mode}" />')
    if api_path_strip is not None:
        meta_extra.append(f'<meta name="fastui:APIPathStrip" content="{api_path_strip}" />')
    meta_extra_str = '\n    '.join(meta_extra)
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
    {meta_extra_str}
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
"""
