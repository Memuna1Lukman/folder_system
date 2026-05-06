from pydantic import EmailStr,BaseModel
from typing import Optional
from datetime import datetime

class TokenData(BaseModel):
    id: Optional[int]


class User(BaseModel):
    id: Optional[int] = None
    email : str
    username : str
    password : str
    is_active : Optional[bool] = None

class UserResponse(BaseModel):
    id : Optional[int] = None
    username : str
    is_active : Optional[bool] = None
    model_config = {"from_attributes": True}

class Folder(BaseModel):
    id : Optional[int] = None
    name : str
    owner_id : Optional[int] = None
    created_at : Optional[datetime] = None

class FolderResponse(Folder):
    pass
    model_config = {"from_attributes": True}

class Documents(BaseModel):
    id : Optional[int] = None
    title : str
    content : str
    folder_id : int
    owner_id : Optional[int]
    created_at : Optional[datetime] = None
    updated_at : Optional[datetime] = None

class DocResponse(Documents):
    pass
    model_config = {"from_attributes": True}
