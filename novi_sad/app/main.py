from datetime import datetime
from fastapi import FastAPI, HTTPException
from psycopg.rows import class_row
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


# class Reservation(BaseModel):
#     bike_id: uuid.UUID
#     user_id: uuid.UUID
#     type: str
#     date: datetime


@app.post("/users")
async def create_user(user: User):
    async with httpx.AsyncClient() as client:
        # print("sending request")
        # print("nigga")
        response = await client.post(
            f"http://{os.environ["CENTRAL_SERVER_HOST"]}:{os.environ["CENTRAL_SERVER_PORT"]}/users",
            json=user.model_dump(),
        )
        print(response.content)
        if response.is_error:
            raise HTTPException(
                status_code=400,
                detail=json.loads(response.content)["detail"],
            )
        return response.content
