import os
import secrets
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime

import libsql_client


@dataclass
class User:
    token: str
    email: str
    last_active: datetime


async def get_user(token: str) -> User | None:
    async with _connect() as conn:
        rs = await conn.execute('select * from users where token = ?', (token,))
        if rs.rows:
            await conn.execute('update users set last_active = current_timestamp where token = ?', (token,))
            return User(*rs.rows[0])


async def create_user(email: str) -> str:
    async with _connect() as conn:
        await _delete_old_users(conn)
        token = secrets.token_hex()
        await conn.execute('insert into users (token, email) values (?, ?)', (token, email))
        return token


async def delete_user(user: User) -> None:
    async with _connect() as conn:
        await conn.execute('delete from users where token = ?', (user.token,))


async def count_users() -> int:
    async with _connect() as conn:
        await _delete_old_users(conn)
        rs = await conn.execute('select count(*) from users')
        return rs.rows[0][0]


async def create_db() -> None:
    async with _connect() as conn:
        rs = await conn.execute("select 1 from sqlite_master where type='table' and name='users'")
        if not rs.rows:
            await conn.execute(SCHEMA)


SCHEMA = """
create table if not exists users (
    token varchar(255) primary key,
    email varchar(255) not null unique,
    last_active timestamp not null default current_timestamp
);
"""


async def _delete_old_users(conn: libsql_client.Client) -> None:
    await conn.execute('delete from users where last_active < datetime(current_timestamp, "-1 hour")')


@asynccontextmanager
async def _connect() -> libsql_client.Client:
    auth_token = os.getenv('SQLITE_AUTH_TOKEN')
    if auth_token:
        url = 'libsql://fastui-samuelcolvin.turso.io'
    else:
        url = 'file:users.db'
    async with libsql_client.create_client(url, auth_token=auth_token) as conn:
        yield conn
