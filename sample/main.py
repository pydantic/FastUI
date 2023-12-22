from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    dob: date = Field(title="Date of Birth")


# define some users
users = [
    User(id=1, name="John", dob=date(1990, 1, 1)),
    User(id=2, name="Jack", dob=date(1991, 1, 1)),
    User(id=3, name="Jill", dob=date(1992, 1, 1)),
    User(id=4, name="Jane", dob=date(1993, 1, 1)),
]

app = FastAPI()


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def users_table() -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text="Users", level=2),  # renders `<h2>Users</h2>`
                c.Table(  # c.Table is a generic component parameterized with the model used for rows
                    data=users,
                    data_model=User,  # data_model defines a model used for rows
                    # define two columns for the table
                    columns=[
                        # the first is the users, name rendered as a link to their profile
                        DisplayLookup(
                            field="name", on_click=GoToEvent(url="/user/{id}/")
                        ),
                        # the second is the date of birth, rendered as a date
                        DisplayLookup(field="dob", mode=DisplayMode.date),
                    ],
                ),
            ]
        ),
    ]


@app.get(
    "/api/user/{user_id}/", response_model=FastUI, response_model_exclude_none=True
)
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
                c.Link(components=[c.Text(text="Back")], on_click=BackEvent()),
                c.Details(data=user),
            ]
        ),
    ]


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title="FastUI Demo"))
