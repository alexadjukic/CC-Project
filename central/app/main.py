from datetime import datetime
from fastapi import FastAPI, HTTPException
from psycopg import Error
from psycopg.rows import class_row
from pydantic import BaseModel, StringConstraints
from typing import Annotated
import uuid
import json
from .db import pool

app = FastAPI()


class User(BaseModel):
    jmbg: Annotated[str, StringConstraints(pattern=r"^\d{13}$")]
    name: Annotated[str, StringConstraints(max_length=50)]
    surname: Annotated[str, StringConstraints(max_length=50)]
    address: Annotated[str, StringConstraints(max_length=150)]
    # bikes_rented: Annotated[int, Field(gt=-1, lt=3)]


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
            except Error as e:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        e.diag.message_detail
                        if e.diag.message_detail
                        else e.diag.message_primary
                    ),
                )


@app.get("/users")
async def get_users():
    with pool.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")

        return cur.fetchall()


@app.put("/users/rent")
async def rent_bike(jmbg: Annotated[str, StringConstraints(pattern=r"^\d{13}$")]):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE public.users SET bikes_rented=bikes_rented+1 WHERE jmbg=%s;",
                    (jmbg,),
                )
            except Error as e:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        e.diag.message_detail
                        if e.diag.message_detail
                        else e.diag.message_primary
                    ),
                )


@app.put("/users/return")
async def return_bike(jmbg: Annotated[str, StringConstraints(pattern=r"^\d{13}$")]):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE public.users SET bikes_rented=bikes_rented-1 WHERE jmbg=%s;",
                    (jmbg,),
                )
            except Error as e:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        e.diag.message_detail
                        if e.diag.message_detail
                        else e.diag.message_primary
                    ),
                )
