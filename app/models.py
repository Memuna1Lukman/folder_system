from sqlalchemy import Column,Integer,String,text,TIMESTAMP,ForeignKey,Boolean
from .database import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    username = Column(String,index=True,unique=True,nullable=False)
    email = Column(String,index=True,unique=True,nullable=False)
    password = Column(String,nullable=False)
    is_active = Column(Boolean,server_default='TRUE',nullable=False)
    folders = relationship("Folders",back_populates="owner")
    documents = relationship("Document", back_populates="owner")
    shared_access = relationship("Permissions", back_populates="user")


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer,primary_key=True)
    name = Column(String,index=True,nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    owner = relationship("User",back_populates="folders")
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))  
    documents = relationship("Document", back_populates="folder")
    


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer,primary_key=True)
    title = Column(String,index=True,nullable=False)
    content = Column(String,nullable=False)
    folder_id = Column(Integer,ForeignKey("folders.id",ondelete='CASCADE'),nullable=False)
    folder = relationship("Folders" , back_populates="documents")
    owner_id = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    owner = relationship("User", back_populates="documents")
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))  
    updated_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
    permissions = relationship("Permissions", back_populates="document")



class Permissions(Base):
    __tablename__ = "permissions"


    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    document_id = Column(Integer,ForeignKey("documents.id",ondelete='CASCADE'),nullable=False)
    access_level = Column(String,nullable=False)
    user = relationship("User", back_populates="shared_access")
    document = relationship("Document", back_populates="permissions")