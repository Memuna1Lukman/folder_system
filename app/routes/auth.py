from fastapi import APIRouter,HTTPException,Depends,status
from  .. import models,schemas,oauth,utils
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/login",
    tags=['Log In']
)


@router.post("/")
def login_user(user:OAuth2PasswordRequestForm= Depends(),db:Session = Depends(get_db)):
    try:
        query_user = db.query(models.User).filter(models.User.email == user.username).first()
        if not query_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are an authorized user")
        verify_password = utils.unhash_password(user.password,query_user.password)
        if not verify_password:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are an authorized user")
        access_token = oauth.create_access_token(data={"user_id":query_user.id})
    except TypeError as e:
        print("You have incurred an error")
        print(e)

    return {"token": access_token,"token_type":"bearer"}

