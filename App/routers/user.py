from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from App.database import get_db
from App import models, schemas, utils

router = APIRouter(
    prefix="/users", #abstracts away the need to write "/posts" in every single api route
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user( user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password - user.password
    hashed_pw = utils.hash(user.password) #1st we hash the pw
    user.password = hashed_pw #then we store it in user password

    new_user =  models.User(**user.dict()) 

    db.add(new_user) 
    db.commit()
    db.refresh(new_user)  
    return new_user 

@router.get("/{id}", response_model=schemas.UserOut) 
def get_user(id: int, db: Session = Depends(get_db)):
   user = db.query(models.User).filter(models.User.id == id).first() 

   if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id: {id} does not exist.")
   return user 