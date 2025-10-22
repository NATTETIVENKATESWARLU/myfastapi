from random import *
from typing import Optional
from fastapi import FastAPI,HTTPException,Request,Response,status
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
import time


app = FastAPI()

class Posts(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: Optional[str] = None

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fast_api",
            user="postgres",
            password="root",
            cursor_factory=RealDictCursor
        )
        print("Database connection successful")
        break
    except Exception as e:
            print(f"Database connection failed: {e}")
            time.sleep(2)

#----------------------------------------------------------------------------------------
# First root endpoint which path is first in order that will execute first
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Second root endpoint for demonstration purposes
@app.get("/")
async def read_root1():
    return {"message": "This is the second root endpoint."}
#----------------------------------------------------------------------------------------

#add post request endpoint
@app.post("/items/")
async def create_item(payload: dict = Body(...)):
    print(payload)
    return {"message": "Item created successfully!", "item": payload}


#add another post request endpoint ui asking payload from request
@app.post("/items1/")
async def create_item1(request: Request):
    payload = await request.json()
    print(payload)
    return {"message": "Item created successfully!", "item": payload}


# Endpoint to validate item using Pydantic model
@app.post("/items2/")
async def create_item2(item: Posts):
    print(item)
    print(item.title)
    print(item.dict())
    return {"item": item}


#----------------------------------------------------------------------------------------
#crud operation endpoints
mypost=[{"id":1,"title":"first post","content":"this is the content of the first post"},
        {"id":2,"title":"second post","content":"this is the content of the second post"},
        {"id":3,"title":"third post","content":"this is the content of the third post"},
        {"id":4,"title":"fourth post","content":"this is the content of the fourth post"},
        {"id":5,"title":"fifth post","content":"this is the content of the fifth post"}]

async def get_post(id: int):
    for post in mypost:
        if post["id"]==id:
            return post
    return None

async def find_index_post(id: int):
    for i, post in enumerate(mypost):
        if post["id"]==id:
            return i
    return None

@app.get("/myposts/")
async def get_posts():
    return {"mypost": mypost}



@app.get("/myposts/{id}")
# async def get_post_by_id(id: int, response: Response):
async def get_post_by_id(id: int):
    post = await get_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Post with id {id} not found"}
    return {"post": post}


#latest data
@app.get("/myposts/latest/")
async def get_latest_posts():
    mydata=mypost[-1]
    return {"latest_posts": mydata}




@app.post("/myposts/",status_code=status.HTTP_201_CREATED)
async def create_item3(item: Posts):
    public_data = item.dict()
    public_data["id"]=randint(1,1000)
    mypost.append(public_data)
    return {"item": public_data}


@app.delete("/myposts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = await find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    mypost.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/myposts/{id}")
async def update_post(id: int, item: Posts):
    index = await find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    updated_post = item.dict()
    updated_post["id"] = id
    mypost[index] = updated_post
    return {"post": updated_post}

@app.patch("/myposts/{id}")
async def patch_post(id: int, item: Posts):
    index = await find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    stored_post_data = mypost[index]
    stored_post_model = Posts(**stored_post_data)
    update_data = item.dict(exclude_unset=True)
    updated_post = stored_post_model.copy(update=update_data)
    mypost[index] = updated_post.dict()
    mypost[index]["id"] = id
    return {"post": mypost[index]}

#----------------------------------------------------------------------------------------
#data base connection endpoints
@app.get("/db/data/")
async def get_db_data():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts;")
    
    data = cursor.fetchall()
    print(data)
    return {"data": data}

#single data retrieval from database
@app.get("/db/data/{id}")
async def get_db_data_by_id(id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = %s;", (id,))
    
    data = cursor.fetchone()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    return {"data": data}


@app.post("/db/data/",status_code=status.HTTP_201_CREATED)
async def create_db_data(item: Posts):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;",(item.title, item.content, item.published))
    new_data = cursor.fetchone()
    conn.commit()
    print(new_data)
    return {"data": new_data}

@app.put("/db/data/{id}")
async def update_db_data(id: int, item: Posts):
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;",(item.title, item.content, item.published, id))
    updated_data = cursor.fetchone()
    conn.commit()
    if not updated_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    print(updated_data)
    return {"data": updated_data}

@app.patch("/db/data/{id}")
async def patch_db_data(id: int, item: Posts):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = %s;", (id,))
    stored_data = cursor.fetchone()
    if not stored_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    updated_title = item.title if item.title is not None else stored_data['title']
    updated_content = item.content if item.content is not None else stored_data['content']
    updated_published = item.published if item.published is not None else stored_data['published']
    
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;",(updated_title, updated_content, updated_published, id))
    updated_data = cursor.fetchone()
    conn.commit()
    print(updated_data)
    return {"data": updated_data}

@app.delete("/db/data/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_db_data(id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (id,))
    deleted_data = cursor.fetchone()
    conn.commit()
    if not deleted_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)