from fastapi import FastAPI,Response,status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schema
from .database import engine,get_db
from sqlalchemy.orm import Session
from typing import List

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


        


@app.get("/")
async def root():
    return {"message": "Welcome to my API!!"}


@app.get('/posts',response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts


@app.post('/posts',status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_post(post:schema.PostCreate,db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get('/posts/{id}',response_model=schema.Post)
def get_post(id:int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")

    return post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schema.Post)
def update_post(id:int,updated_post:schema.PostCreate,db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    post_query.update(updated_post.dict(),
                      synchronize_session = False)
    db.commit()
    return post_query.first()
