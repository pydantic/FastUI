# FastUI

[![CI](https://github.com/pydantic/FastUI/actions/workflows/ci.yml/badge.svg)](https://github.com/pydantic/FastUI/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![pypi](https://img.shields.io/pypi/v/fastui.svg)](https://pypi.python.org/pypi/fastui)
[![versions](https://img.shields.io/pypi/pyversions/fastui.svg)](https://github.com/pydantic/FastUI)
[![license](https://img.shields.io/github/license/pydantic/FastUI.svg)](https://github.com/pydantic/FastUI/blob/main/LICENSE)

**Please note:** FastUI is still an active work in progress, do not expect it to be complete.

## The Principle (short version)

You can see a simple demo of an application built with FastUI [here](https://fastui-demo.onrender.com).

FastUI is a new way to build web application user interfaces defined by declarative Python code.

This means:

- **If you're a Python developer** — you can build responsive web applications using React without writing a single line of JavaScript, or touching `npm`.
- **If you're a frontend developer** — you can concentrate on building magical components that are truly reusable, no copy-pasting components for each view.
- **For everyone** — a true separation of concerns, the backend defines the entire application; while the frontend is free to implement just the user interface

At its heart, FastUI is a set of matching [Pydantic](https://docs.pydantic.dev) models and TypeScript interfaces that allow you to define a user interface. This interface is validated at build time by TypeScript and pyright/mypy and at runtime by Pydantic.

## The Practice — Usage

FastUI is made up of 4 things:

- [`fastui` PyPI package](https://pypi.python.org/pypi/fastui) — Pydantic models for UI components, and some utilities. While it works well with [FastAPI](https://fastapi.tiangolo.com) it doesn't depend on FastAPI, and most of it could be used with any python web framework.
- [`@pydantic/fastui` npm package](https://www.npmjs.com/package/@pydantic/fastui) — a React TypeScript package that lets you reuse the machinery and types of FastUI while implementing your own components
- [`@pydantic/fastui-bootstrap` npm package](https://www.npmjs.com/package/@pydantic/fastui-bootstrap) — implementation/customisation of all FastUI components using [Bootstrap](https://getbootstrap.com)
- [`@pydantic/fastui-prebuilt` npm package](https://www.jsdelivr.com/package/npm/@pydantic/fastui-prebuilt) (available on [jsdelivr.com CDN](https://www.jsdelivr.com/package/npm/@pydantic/fastui-prebuilt)) providing a pre-built version of the FastUI React app so you can use it without installing any npm packages or building anything yourself. The Python package provides a simple HTML page to serve this app.

Here's a simple but complete FastAPI application that uses FastUI to show some user profiles:

```python
from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    dob: date = Field(title='Date of Birth')


# define some users
users = [
    User(id=1, name='John', dob=date(1990, 1, 1)),
    User(id=2, name='Jack', dob=date(1991, 1, 1)),
    User(id=3, name='Jill', dob=date(1992, 1, 1)),
    User(id=4, name='Jane', dob=date(1993, 1, 1)),
]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def users_table() -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Users', level=2),  # renders `<h2>Users</h2>`
                c.Table(
                    data=users,
                    # define two columns for the table
                    columns=[
                        # the first is the users, name rendered as a link to their profile
                        DisplayLookup(field='name', on_click=GoToEvent(url='/user/{id}/')),
                        # the second is the date of birth, rendered as a date
                        DisplayLookup(field='dob', mode=DisplayMode.date),
                    ],
                ),
            ]
        ),
    ]


@app.get("/api/user/{user_id}/", response_model=FastUI, response_model_exclude_none=True)
def user_profile(user_id: int) -> list[AnyComponent]:
    """
    User profile page, the frontend will fetch this when the user visits `/user/{id}/`.
    """
    try:
        user = next(u for u in users if u.id == user_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="User not found")
    return [
        c.Page(
            components=[
                c.Heading(text=user.name, level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Details(data=user),
            ]
        ),
    ]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))
```

Which renders like this:

![screenshot](https://raw.githubusercontent.com/pydantic/FastUI/main/screenshot.png)

Of course, that's a very simple application, the [full demo](https://fastui-demo.onrender.com) is more complete.

### Components

FastUI already defines a rich set of components.

All components are listed in the [demo app](https://fastui-demo.onrender.com).

## The Principle (long version)

FastUI is an implementation of the RESTful principle; but not as it's usually understood, instead I mean the principle defined in the original [PhD dissertation](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) by Roy Fielding, and excellently summarised in [this essay on htmx.org](https://htmx.org/essays/how-did-rest-come-to-mean-the-opposite-of-rest/) (HTMX people, I'm sorry to use your article to promote React which I know you despise 🙏).

The RESTful principle as described in the HTMX article is that the frontend doesn't need to (and shouldn't) know anything about the application you're building. Instead, it should just provide all the components you need to construct the interface, the backend can then tell the frontend what to do.

Think of your frontend as a puppet, and the backend as the hand within it — the puppet doesn't need to know what to say, that's kind of the point.

Building an application this way has a number of significant advantages:

- You only need to write code in one place to build a new feature — add a new view, change the behavior of an existing view or alter the URL structure
- Deploying the front and backend can be completely decoupled, provided the frontend knows how to render all the components the backend is going to ask it to use, you're good to go
- You should be able to reuse a rich set of opensource components, they should end up being better tested and more reliable than anything you could build yourself, this is possible because the components need no context about how they're going to be used (note: since FastUI is brand new, this isn't true yet, hopefully we get there)
- We can use Pydantic, TypeScript and JSON Schema to provide guarantees that the two sides are communicating with an agreed schema (note: this is not complete yet, see [#18](https://github.com/pydantic/FastUI/issues/18))

In the abstract, FastUI is like the opposite of GraphQL but with the same goal — GraphQL lets frontend developers extend an application without any new backend development; FastUI lets backend developers extend an application without any new frontend development.

### Beyond Python and React

Of course, this principle shouldn't be limited to Python and React applications — provided we use the same set of agreed schemas and encoding to communicate, we should be able to use any frontend and backend that implements the schema. Interchangeably.

This could mean:

- Implementing a web frontend using another JS framework like Vue — lots of work, limited value IMHO
- Implementing a web frontend using an edge server, so the browser just sees HTML — lots of work but very valuable
- Implementing frontends for other platforms like mobile or IOT — lots of work, no idea if it's actually a good idea?
- Implementing the component models in another language like Rust or Go — since there's actually not that much code in the backend, so this would be a relatively small and mechanical task
