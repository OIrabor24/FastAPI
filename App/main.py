from fastapi import FastAPI
from psycopg2.extras import RealDictCursor #we need this import to get the column names from our database
import time 
from sqlalchemy.orm import Session
from App import models
from App.database import engine
from App.routers import post, user, auth, vote
from App.config import settings
from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind=engine) # Code that creates our tables


app = FastAPI()

origins = ["*"]

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

@app.get("/") #app comes from our app name above
def root():

    return {"message": "Welcome to my instance of FastAPI!"} 





