from jose import JWSError,jwt
from . import models,schemas
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from datetime import datetime,timedelta


SECRET_KEY = settings.secret_key

ALGORITHM = settings.algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})

    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt


def verify_access_token(token:str,credentail_exceptions):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str = payload.get("user_id")
        if id is None:
            raise credentail_exceptions
        tokens = schemas.TokenData(id=id)
    except JWSError as e:   
        print(e)
        raise credentail_exceptions
    
    return tokens




def get_current_user(token:str = Depends(oauth_scheme),db:Session= Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token= verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

