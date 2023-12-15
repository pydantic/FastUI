import secrets
from dataclasses import dataclass
from datetime import datetime

from aiosqlite import connect


@dataclass
class User:
    token: str
    email: str
    last_active: datetime


async def get_user(token: str) -> User | None:
    async with connect('users.db') as conn:
        async with conn.execute('select * from users where token = ?', (token,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return User(*row)


async def save_user(email: str) -> str:
    async with connect('users.db') as conn:
        token = secrets.token_hex()
        await conn.execute(
            'insert into users (token, email) values (?, ?)',
            (token, email),
        )
        await conn.commit()
        return token


async def delete_user(user: User) -> None:
    async with connect('users.db') as conn:
        await conn.execute('delete from users where token = ?', (user.token,))
        await conn.commit()


async def count_users() -> int:
    async with connect('users.db') as conn:
        async with conn.execute('select count(*) from users') as cursor:
            return (await cursor.fetchone())[0]


SCHEMA = """
create table if not exists users (
    token varchar(255) primary key,
    email varchar(255) not null unique,
    last_active timestamp not null default current_timestamp
);
"""
