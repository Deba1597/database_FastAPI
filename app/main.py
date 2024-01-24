from typing import Optional
from fastapi import FastAPI,Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool =True
    rating : Optional[int]=None



my_post = [{'title':"title of post 1","content":"Content of post 1","id":1},
           {'title':"favourite food","content":"i like pizza","id":2}]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Welcome to my API!!"}

@app.get('/posts')
def get_posts():
    return {'data': my_post}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_post(new_post:Post):
    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(0,100000)
    my_post.append(post_dict)
    return {'data':post_dict}


@app.get('/posts/{id}')
def get_post(id:int,response: Response):
    post = find_post(id)
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return {'Post_details': post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #find the index in the array that has required ID
    #my_post.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")

    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    print(post)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {'message':post_dict}
