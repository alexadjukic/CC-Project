from datetime import datetime
from fastapi import FastAPI, HTTPException
from psycopg.rows import class_row
from psycopg import Error
from pydantic import BaseModel, StringConstraints
from typing import Annotated
import uuid
import httpx
import os
import json
from .db import pool

app = FastAPI()


class User(BaseModel):
    jmbg: Annotated[str, StringConstraints(pattern=r"^\d{13}$")]
    name: str
    surname: str
    address: str


class Rental(BaseModel):
    bike_id: uuid.UUID
    jmbg: Annotated[str, StringConstraints(pattern=r"^\d{13}$")]
    type: str
    # date: datetime


@app.post("/users")
async def create_user(user: User):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{os.environ["CENTRAL_SERVER_HOST"]}:{os.environ["CENTRAL_SERVER_PORT"]}/users",
            json=user.model_dump(),
        )
        if response.is_error:
            raise HTTPException(
                status_code=400,
                detail=json.loads(response.content)["detail"],
            )
        return json.loads(response.content)


@app.post("/rental")
async def rent_bike(rental: Rental):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"http://{os.environ["CENTRAL_SERVER_HOST"]}:{os.environ["CENTRAL_SERVER_PORT"]}/users/rent?jmbg={rental.jmbg}",
        )

        if response.is_error:
            raise HTTPException(
                status_code=400, detail=json.loads(response.content)["detail"]
            )

        with pool.connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        "INSERT INTO rentals (bike_id, jmbg, type, date) VALUES (%s, %s, %s, %s) RETURNING bike_id, jmbg;",
                        (rental.bike_id, rental.jmbg, rental.type, datetime.now()),
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

                return cur.fetchone()


@app.delete("/return")
async def return_bike(
    jmbg: Annotated[str, StringConstraints(pattern=r"^\d{13}$")], bike_id: uuid.UUID
):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"http://{os.environ["CENTRAL_SERVER_HOST"]}:{os.environ["CENTRAL_SERVER_PORT"]}/users/return?jmbg={jmbg}&bike_id={bike_id}",
        )

        if response.is_error:
            raise HTTPException(
                status_code=400, detail=json.loads(response.content)["detail"]
            )

        with pool.connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        "DELETE FROM rentals WHERE jmbg=%s AND bike_id=%s;",
                        (jmbg, bike_id),
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


@app.get("/rentals")
async def get_rentals():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM rentals;")

            return cur.fetchall()
