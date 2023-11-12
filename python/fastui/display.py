from enum import StrEnum


class Display(StrEnum):
    """
    How to a value.
    """

    auto = 'auto'  # default, same as None below
    plain = 'plain'
    datetime = 'datetime'
    date = 'date'
    duration = 'duration'
    as_title = 'as_title'
    markdown = 'markdown'
    json = 'json'
    inline_code = 'inline_code'
