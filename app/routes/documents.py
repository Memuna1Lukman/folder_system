from fastapi import APIRouter,Depends,HTTPException,status
from ..database import get_db
from .. import models,schemas,oauth
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime,timezone
router = APIRouter(
    prefix="/document",
    tags=['Documents']
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.DocResponse)
def create_documents(
    doc:schemas.Documents,
    db:Session = Depends(get_db),
    current_user: models.User = Depends(oauth.get_current_user)
):
    # Does the folder exist
    # Does the user still exist
    #  is the user authorized
    
    query_folder = db.query(models.Folder).filter(models.Folder.id == doc.folder_id).first()
    if not query_folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"folder with id {doc.folder_id} not found")
    if query_folder.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Must be an authorized user")
    
    doc_dict = models.Document(title=doc.title,content=doc.content,folder_id=doc.folder_id,owner_id = current_user.id)
    db.add(doc_dict)
    db.commit()
    db.refresh(doc_dict)
    return doc_dict


@router.get("/",response_model=List[schemas.DocResponse])
def get_my_docments(
    db:Session = Depends(get_db),
    current_user:int = Depends(oauth.get_current_user),
    limit: int = 10,
    skip:int = 0
):
    query_doc = db.query(models.Document).filter(models.Document.owner_id == current_user.id).limit(limit).offset(skip).all()
    if not query_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return query_doc

@router.get("/search/{title}",response_model=List[schemas.DocResponse])
def search_document(
    title:str,
    db:Session = Depends(get_db),
    current_user:int = Depends(oauth.get_current_user)
):
    query_docs = db.query(models.Document).filter(
        models.Document.owner_id == current_user.id,
        models.Document.title.ilike(f"%{title}%")
    ).all()
    if not query_docs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Docuument not available")
    return query_docs
    

@router.put("/{id}",response_model=schemas.DocResponse)
def upd_doc(
    id :int,
    doc:schemas.Documents,
    db:Session = Depends(get_db),
    current_user:int = Depends(oauth.get_current_user)
):
    # Check if that id belongs to this person
    # check if the folder exist
    # cheeck if thee user is authorized

    query_docs = db.query(models.Document).filter(
        models.Document.id == id
    )
    query = query_docs.first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Must be an authorized user")
    update_data = doc.dict(exclude_unset=True)
    update_data['updated_at'] = datetime.now(timezone.utc)
    query_docs.update(update_data,synchronize_session=False)
    db.commit()
    db.refresh(query)
    return query
    