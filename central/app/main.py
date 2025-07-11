from datetime import datetime
from fastapi import FastAPI
from psycopg.rows import class_row
from pydantic import BaseModel, StringConstraints
from typing import Annotated
import uuid
from .db import pool

app = FastAPI()


class User(BaseModel):
    jmbg: Annotated[str, StringConstraints(pattern=r"^\d{13}$")]
    # id: uuid.UUID = uuid.uuid4()
    name: str
    surname: str
    address: str


class Reservation(BaseModel):
    bike_id: uuid.UUID
    user_id: uuid.UUID
    type: str
    date: datetime


@app.post("/users")
def create_user(user: User):
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO public.users(name, surname, address, jmbg) VALUES (%s, %s, %s, %s) RETURNING id;",
            (user.name, user.surname, user.address, user.jmbg),
        )
        return cur.fetchone()


@app.get("/users")
async def get_users():
    with pool.connection() as conn:
        cur = conn.cursor(row_factory=class_row(User))
        cur.execute("SELECT * FROM users;")

        return cur.fetchall()
