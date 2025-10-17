from fastapi import FastAPI,HTTPException

app = FastAPI()

# First root endpoint which path is first in order that will execute first
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Second root endpoint for demonstration purposes
@app.get("/")
async def read_root1():
    return {"message": "This is the second root endpoint."}