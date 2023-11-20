from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import config
import schema
from database import config
from models import models
# tokenUrl is the name of login route then we will use it in the login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# secret key . we need to generate a secret key and use it to sign our JWT tokens.
SECRET_KEY = "09D23e3sdsa23kj2323jh23g2h3g2h3g2h323g2h3g2h3g2"
# algorithm used to sign the JWT tokens. We will use HS256, which is a symmetric algorithm.
ALGORITHM = "HS256"
# expiration time for our JWT tokens. We will set it to 15 minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(data: dict):
    to_encode = data.copy()
    # set the expiration time for the JWT token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # add the expiration time to the JWT token
    to_encode.update({"exp": expire})
    # encode the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # return the JWT token
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schema.TokenData(user_id=user_id)
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(config.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(
        models.User.id == token.user_id).first()
    return user
