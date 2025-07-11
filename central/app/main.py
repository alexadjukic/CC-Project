from datetime import datetime
from fastapi import FastAPI, HTTPException
from psycopg.rows import class_row
from psycopg.errors import UniqueViolation
from pydantic import BaseModel, StringConstraints
from typing import Annotated
import uuid
from .db import pool

app = FastAPI()


class User(BaseModel):
    jmbg: Annotated[str, StringConstraints(pattern=r"^\d{13}$")]
    name: str
    surname: str
    address: str


class Reservation(BaseModel):
    bike_id: uuid.UUID
    user_id: uuid.UUID
    type: str
    date: datetime


@app.post("/users")
async def create_user(user: User):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO public.users(jmbg, name, surname, address) VALUES (%s, %s, %s, %s) RETURNING jmbg;",
                    (user.jmbg, user.name, user.surname, user.address),
                )
                return cur.fetchone()
            except UniqueViolation as e:
                print(e.args)
                raise HTTPException(
                    status_code=400, detail=e.args[0].split("DETAIL:  ")[1]
                )


@app.get("/users")
async def get_users():
    with pool.connection() as conn:
        cur = conn.cursor(row_factory=class_row(User))
        cur.execute("SELECT * FROM users;")

        return cur.fetchall()
