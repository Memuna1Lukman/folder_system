from fastapi import APIRouter,Depends,HTTPException,status
from ..database import get_db
from .. import models,schemas,utils
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/signup",
    tags= ['Sign Up']
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def sign_up_user (user:schemas.User,db:Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user_dict = user.dict()
    user_dict['password'] = hashed_password
    user_dict = models.User(**user_dict)
    db.add(user_dict)
    db.commit()
    db.refresh(user_dict)
    return user_dict

