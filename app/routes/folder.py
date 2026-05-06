from fastapi import APIRouter,Depends,HTTPException,status
from ..database import get_db
from .. import models,schemas,oauth
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/folder",
    tags= ['Folders']
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.FolderResponse)
def create_folder(folder: schemas.Folder,db:Session = Depends(get_db),current_user:int = Depends(oauth.get_current_user)):
    try:
        query_user = db.query(models.User).filter(models.User.id == folder.owner_id).first()
        if not query_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{folder.owner_id} not found")
        query_current = db.query(models.Folder).filter(models.Folder.owner_id == current_user.id).first()
        if not query_current:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are an authorized user")
        add_folder = models.Folder(owner_id = current_user.id,name=folder.name)
    except TypeError as e:
        print("There is a type error")
        print(e)
    db.add(add_folder)
    db.commit()
    db.refresh(add_folder)
    return add_folder 

@router.get("/",response_model=List[schemas.FolderResponse])
def get_my_folders(db:Session= Depends(get_db),current_user:int=Depends(oauth.get_current_user)):
    try:
        # query_current = db.query(models.User).filter(models.User.id == current_user.id).first()
        # if not query_current:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are an authorized user")
        query_folder = db.query(models.Folder).filter(models.Folder.owner_id == current_user.id).all()
        # if query_folder == []:
        #     raise HTTPException(status_code=status.HTTP_200_OK,detail=[])
        if not query_folder:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are an authorized user")
        
    except TypeError as e:
        print("Error occured")
        print(e)
    return query_folder

@router.delete(
    "/{id}"
)
def delete_folder(
    id:int,
    db:Session =Depends(get_db),
    current_user:int = Depends(oauth.get_current_user)
):
    try:
        # query_user = db.query(models.User).filter(models.User.id == current_user.id).first()
        # if not query_user:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} not found")
        query_user_folders = db.query(models.Folder).filter(models.Folder.id==id)
        query = query_user_folders.first()
        # if query == []:
        #     raise HTTPException(status_code=status.HTTP_200_OK,detail=[])
        if query.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are an authorized user")
        if query == None:
                raise HTTPException(status_code = 404,detail = f"the post witht he {id} is not found")

    except TypeError as e:
        print (e)
        print("Error occured")

    db.delete(query,synchronize_session=False)
    db.commit()
    return None              

        
        
