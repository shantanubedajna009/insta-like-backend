from typing import List
from fastapi import APIRouter, Depends
from schemas import CommentDisplay, CommentRequest, CommentRequestForUpdate
from database.db import get_db
from sqlalchemy.orm.session import Session
from authentication.auth import get_current_user_from_token
from schemas import UserAuth
from database.comment_operations import (create_comment,
                                         get_single_comment,
                                         get_allcomments_for_post,
                                         delete_comment,
                                         update_comment
                                        )

router = APIRouter(
    prefix='/comments',
    tags=['Comments']
)


@router.post('/new', response_model=CommentDisplay)
def api_create_comment(request: CommentRequest,
                     db: Session = Depends(get_db), 
                     current_user: UserAuth = Depends(get_current_user_from_token)):
    return create_comment(request, db, current_user.username)

@router.get('/{id}', response_model=CommentDisplay)
def api_get_comment(id: int, db: Session = Depends(get_db)):
    return get_single_comment(id, db)

@router.get('/{post_id}/all', response_model=List[CommentDisplay])
def api_get_post_comments(post_id: int, 
                        db: Session = Depends(get_db)):
    return get_allcomments_for_post(post_id, db)

@router.delete('/delete/{id}')
def api_delete_comment(id: int, db: Session = Depends(get_db),
                         current_user: UserAuth = Depends(get_current_user_from_token)):
    return delete_comment(id, db, current_user.username)

@router.post('/update/{id}', response_model=CommentDisplay)
def api_update_comment(id: int, request: CommentRequestForUpdate,
                         db: Session = Depends(get_db), 
                         current_user: UserAuth = Depends(get_current_user_from_token)):
    
    return update_comment(id, request, db, current_user.username)