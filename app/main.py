from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from . import models,schemas
from .database import SessionLocal
import psycopg2
from .routes import auth,users,folder,documents,permission

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(folder.router)
app.include_router(documents.router)
app.include_router(permission.router)