from fastapi import FastAPI,Response, status, HTTPException,APIRouter
from fastapi import Body,Depends
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from schema import CreatePost,ResponsePost,UserCreate,UserOut
from models import models
from database.config import engine, get_db
from sqlalchemy.orm import Session
import utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hashed_password
    try:
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Error while creating user {error.__cause__}")
    
@router.get("/{user_id}",response_model=UserOut)
def get_user(user_id:int,db: Session = Depends(get_db)):
    #buna da sdece registered user dememiz lazim. hatta role admin olmali.
    selected_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not selected_user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return selected_user