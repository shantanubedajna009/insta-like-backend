import shutil
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from schemas import PostDisplaySchema, PostRequest
from sqlalchemy.orm.session import Session
from database.db import get_db
from database.post_operations import create_post, get_all_posts, delete_post, update_post
import uuid
from authentication.auth import get_current_user_from_token
from schemas import UserAuth

router = APIRouter(
    prefix="/post",
    tags=['Post']
)

@router.post('/new', response_model=PostDisplaySchema)
def api_create_post(request: PostRequest, db: Session = Depends(get_db),
                     current_user: UserAuth = Depends(get_current_user_from_token)):
    return create_post(request, db, current_user.id)

@router.get('/all', response_model=List[PostDisplaySchema])
def api_get_all_posts(db: Session = Depends(get_db)):
    return get_all_posts(db)

@router.post('/upload')
def upload_image(file_obj: UploadFile = File(...), 
                current_user: UserAuth = Depends(get_current_user_from_token)):
    pathof = f'images/{uuid.uuid4().hex + "_" + file_obj.filename}'
    with open(pathof, 'w+b') as f:
        shutil.copyfileobj(file_obj.file, f)
    
    return {
        'filename': pathof
    }

@router.post('update/{id}', response_model=PostDisplaySchema)
def api_update_post(id: int, request: PostRequest, db: Session = Depends(get_db),
                     current_user: UserAuth = Depends(get_current_user_from_token)):
    return update_post(id, current_user.id, request, db)

@router.delete('/delete/{id}')
def api_delete_post(id: int, db: Session = Depends(get_db),
                     current_user: UserAuth = Depends(get_current_user_from_token)):  
    return delete_post(id, current_user.id, db)