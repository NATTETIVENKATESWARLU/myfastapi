from random import *
from typing import Optional
from fastapi import FastAPI,HTTPException,Request,Response,status
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]= None
    
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
async def create_item2(item: Item):
    print(item)
    print(item.title)
    print(item.rating)
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
async def create_item3(item: Item):
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
async def update_post(id: int, item: Item):
    index = await find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    updated_post = item.dict()
    updated_post["id"] = id
    mypost[index] = updated_post
    return {"post": updated_post}

@app.patch("/myposts/{id}")
async def patch_post(id: int, item: Item):
    index = await find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    stored_post_data = mypost[index]
    stored_post_model = Item(**stored_post_data)
    update_data = item.dict(exclude_unset=True)
    updated_post = stored_post_model.copy(update=update_data)
    mypost[index] = updated_post.dict()
    mypost[index]["id"] = id
    return {"post": mypost[index]}