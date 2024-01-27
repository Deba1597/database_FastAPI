from fastapi import FastAPI,Response,status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schema,utils
from .database import engine,get_db
from sqlalchemy.orm import Session
from typing import List
from .routers import post,user,auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



while True:   
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi', user='postgres',
                                password='password123',cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print('Database connection was sucessful')
        break
    except Exception as e:
        print('Connecting to database failed')
        print(f'The error was {e}')
        time.sleep(2)



my_post = [{'title':"title of post 1","content":"Content of post 1","id":1},
           {'title':"favourite food","content":"i like pizza","id":2}]


app.include_router(post.router)
app.include_router(user.router)  
app.include_router(auth.router)      


@app.get("/")
async def root():
    return {"message": "Welcome to my API!!"}

