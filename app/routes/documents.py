from fastapi import APIRouter,Depends,HTTPException,status
from ..database import get_db
from .. import models,schemas,oauth
from sqlalchemy.orm import Session
from typing import List