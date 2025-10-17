from fastapi import FastAPI,HTTPException,Request
from fastapi.params import Body

app = FastAPI()

# First root endpoint which path is first in order that will execute first
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Second root endpoint for demonstration purposes
@app.get("/")
async def read_root1():
    return {"message": "This is the second root endpoint."}

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