from random import *
from typing import Optional
from fastapi import FastAPI,HTTPException,Request,Response,status, Depends
from fastapi.params import Body


import time
#----------------------------------------------------------------------------------------
from .schemas import Posts
from .database import engine,Base,get_db
from sqlalchemy.orm import Session
from . import models
#create the database tables
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")
#----------------------------------------------------------------------------------------
app = FastAPI()


#crud operation endpoints using sqlalchemy ORM will be added 

@app.get("/orm/myposts/")
async def get_post_orm(db: Session = Depends(get_db)):
    post = db.query(models.Posts).all()
    return post