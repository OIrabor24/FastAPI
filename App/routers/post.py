from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor #we need this import to get the column names from our database
import time 
from sqlalchemy.orm import Session
from App import models, oauth2, schemas
from App.database import engine, get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", #abstracts away the need to write "/posts" in every single api route
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])  
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] =""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall() 

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
    models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return  posts 


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # default status code for create operation
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user) ): #this is a pydantic model
    """# this extracts all the fields from our post body 
    and converts it into a py dict in the payload""" 
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * 
    # """,
    #     (post.title, post.content, post.published)) #%s matches what we pass in

    # new_post = cursor.fetchone()

    # conn.commit() # we need to run this command to save to our db
    
    new_post =  models.Post(owner_id=current_user.id,**post.dict()) # more efficient than method below
    # new_post =  models.Post(title=post.title, content=post.content, published=post.published) 

    db.add(new_post) # we need to add this created post to the DB
    db.commit() # Then commit it to the DB
    db.refresh(new_post)  #refresh attributes on the given instance.
    return new_post

@router.get("/{id}", response_model=schemas.PostOut) # path parameter; fast api auto grabs the id; validate as #
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):# this syntax auto converts to an int; convert to int
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),)) #; convert back to str

    # test_post = cursor.fetchone()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
    models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} was not found.")
    
    return  post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)): #204 status code for delete operation
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    
    # deleted_post = cursor.fetchone()

    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id {id} does not exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete item") 
   
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) # we don't need to send anything back besides 204
    #when someone deletes something from our routerlication 

@router.put("/{id}", response_model=schemas.Post) 
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):
   
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
    # RETURNING *""",
    #  (post.title, post.content, post.published, str(id))) 

    # updated_post = cursor.fetchone()

    # conn.commit()

    post_query =  db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first() 

    if post == None: #if it does not exist, throw 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id {id} does not exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
         detail="This update action is forbidden")

    post_query.update(updated_post.dict(), synchronize_session=False) 

    db.commit() 
    
    return post_query.first()