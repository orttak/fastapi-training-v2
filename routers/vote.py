from fastapi import FastAPI,Response, status, HTTPException,APIRouter
from fastapi import Body,Depends
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import schema 
from models import models
from database.config import engine, get_db
from sqlalchemy.orm import Session
import utils
import oauth2

router = APIRouter(
    prefix = "/vote",
    tags = ['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote,
         db: Session = Depends(get_db), 
         current_user:int= Depends(oauth2.get_current_user)
         ):
    print("vote",vote)
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id )
    found_vote = vote_query.first()
    if (vote.dir ==1):
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail=f" User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id= vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Succesfully added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_405_NOT_FOUND, detail=f" Vote does not exist") 

        vote_query.delete(synchronize_session= False)
        db.commit()

        return {"message": "Succesfully deleted vote"}

# router.post("/",status_code=status.HTTP_201_CREATED)
# def vote(vote: schema.Vote,
#         #  db: Session = Depends(get_db), 
#         #  current_user:int= Depends(oauth2.get_current_user)
#          ):
#     print("vote",vote)
    # vote_query = db.query(models.Vote).filter(
    #     models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id )
    # found_vote = vote_query.first()
    # if (vote.dir ==1):
    #     if found_vote:
    #         raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail=f" User {current_user.id} has already voted on post {vote.post_id}")
    #     new_vote = models.Vote(post_id= vote.post_id, user_id=current_user.id)
    #     db.add(new_vote)
    #     db.commit()
    #     return {"message": "Succesfully added vote"}
    
    # else:
    #     if not found_vote:
    #         raise HTTPException(status_code = status.HTTP_405_NOT_FOUND, detail=f" Vote does not exist") 

    #     vote_query.delete(synchronize_session= False)
    #     db.commit()

    #     return {"message": "Succesfully deleted vote"}