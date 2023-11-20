from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import config
from models import models
import utils
import schema 
import oauth2
router = APIRouter(
    tags=["Authentication"]
    )


@router.post("/login",status_code=status.HTTP_200_OK,response_model=schema.Token)
def login(user_credential:OAuth2PasswordRequestForm=Depends(), db:Session = Depends(config.get_db)):
    #we change the user_credential.username because of fastapi OAuth2PasswordRequestForm method. we need to be careful about this naming.
    # with this OAuth2PasswordRequestForm method we can get username and password from the body of the request as a form-data
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    print(user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with email {user_credential.email} not found")
    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Password incorrect")
    #create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    #return token
    return {"access_token": access_token, "token_type": "bearer"}
