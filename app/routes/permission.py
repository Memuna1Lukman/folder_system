from fastapi import APIRouter,Depends,HTTPException,status
from ..database import get_db
from .. import models,schemas,oauth
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/permission",
    tags=['Permission']
)


@router.post("/document/{id}/share",response_model=schemas.ShareDocResponse)
def permission(
    id: int,
    doc:schemas.ShareDoc,
    db:Session = Depends(get_db),
    current_user : models.User = Depends(oauth.get_current_user)
):
    #  Is the person making the request the owner_id of the doc
    query_doc = db.query(models.Document).filter(
        models.Document.id == id
    ).first()
    if not query_doc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not permitted to share")
    if query_doc.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can share this document")
    # Target check
    query_user = db.query(models.User).filter(models.User.id == doc.user_id).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Username not found")
    # Conflict check
    existing_permission = db.query(models.Permissions).filter(
        models.Permissions.document_id == id,
        models.Permissions.user_id == doc.user_id
    ).first()
     
    if existing_permission:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Document already shared with this user")
    
    # Adding to permissions table
    

    add_permit = models.Permissions(user_id=doc.user_id,document_id=id,access_level=doc.access_level)
    db.add(add_permit)
    db.commit()
    db.refresh(add_permit)
    return add_permit


@router.get("/document/shared",response_model=List[schemas.ShareDocResponse])
def get_shared_doc(
    db:Session = Depends(get_db),
    current_user : models.User = Depends(oauth.get_current_user)
):
    shared_docs = db.query(models.Permissions).filter(models.Permissions.user_id == current_user.id).all()
    # shared_docs = db.query(models.Document).join(
    #     models.Permissions,models.Document.id == models.Permissions.document_id
    # ).filter(models.Permissions.user_id==current_user.id).all()
    return shared_docs
    # query_permit = db.query(models.Permissions).filter(models.Permissions.owner_id == current_user.id).first()
    # if query_permit:
    #     print("Access granted")
    # else:
    #     query_permission = db.query(models.Permissions).filter(
    #         models.Permissions.user_email== current_user.id,
    #         models.Permissions.document_id == 
    #     )

@router.put("/document/{id}",response_model=schemas.DocResponse)
def permission(
    id: int,
    doc:schemas.Documents,
    db:Session = Depends(get_db),
    current_user : int = Depends(oauth.get_current_user)
):
    query_doc = db.query(models.Document).filter(models.Document.id == id)
    db_doc = query_doc.first()
    if not db_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Document not exist")
    
    is_owner = db_doc.owner_id == current_user.id
    query_perm = db.query(models.Permissions).filter(
        models.Permissions.document_id == id,
        models.Permissions.user_id == current_user.id,
        models.Permissions.access_level == "editor"
    ).first()
    is_editor = query_perm is not None 
    if not is_owner and not is_editor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have permissions to edit this document")
    query_doc.update(doc.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    db.refresh(db_doc)
    return db_doc
    
  