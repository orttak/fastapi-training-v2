import random
import asyncio
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from models import models
from database.config import engine
from routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)


while True:
    try:
        # host,database,username,password
        conn = psycopg2.connect(host="localhost", database="fastapi",
                                user="docker", password="docker", port=32767, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print(" YEYYYYYY Connected to the database")
        break
    except Exception as error:
        print("I am unable to connect to the database")
        print(error)
        time.sleep(5)

app = FastAPI()
origins = ['*'
           # "http://localhost",
           # "http://localhost:8080",
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/random_wait/{id}")
async def random_wait(id: int):
    wait_time = random.randint(0, 30)
    await asyncio.sleep(wait_time)
    return {"id": id, "wait_time": wait_time}
