import datetime
from schemas import CommentRequest, CommentRequestForUpdate
from database.models import DbComment
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session


def create_comment(request: CommentRequest, db: Session, username: str):
    new_comment = DbComment(
        content = request.content,
        username = username,
        post_id = request.post_id,
        timestamp = datetime.datetime.now()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

def get_single_comment(id: int, db: Session):
    comment = db.query(DbComment).filter(DbComment.id == id).first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail='comment with the id does not exist')
    
    return comment

def get_allcomments_for_post(post_id: int, db: Session):
    comments = db.query(DbComment).filter(DbComment.post_id == post_id).all()

    # if not comments:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #      detail='no comments exist with the post id')
    return comments

def delete_comment(id: int, db: Session, username: str):
    comment = db.query(DbComment).filter(DbComment.id == id).first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail='comment with the id does not exist')
    
    if comment.username != username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail='you are not authorized to delete this comment')

    db.delete(comment)
    db.commit()
    return 'ok'

def update_comment(id: int, request: CommentRequestForUpdate, db: Session, username: str):
    comment_update_obj = db.query(DbComment).filter(DbComment.id == id)

    comment = comment_update_obj.first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail='comment with the id does not exist')

    if comment.username != username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail='you are not authorized to Update this comment')

    comment_update_obj.update(
        {
            'content': request.content
        }
    )

    db.commit()

    comment = comment_update_obj.first()
    return comment