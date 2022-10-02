from datetime import datetime
from sqlalchemy.orm.session import Session
from database.models import DbPost
from schemas import PostRequest
from fastapi import status, HTTPException

def create_post(request: PostRequest, db: Session, user_id):
    new_post= DbPost(
        image_url           = request.image_url,
        image_url_type     = request.image_url_type,
        caption             = request.caption,
        date_created        = datetime.now(),
        user_id             = user_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

def delete_post(id: int, user_id: int, db: Session):
    post = db.query(DbPost).filter(DbPost.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'post with id: {id} does not exist')

    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail='post does not belong to the requesting user')

    db.delete(post)
    db.commit()

    return 'ok'

def update_post(id: int, user_id: int, request: PostRequest, db: Session):
    unauthorized_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='You are not authorized to delete this post')
    
    post = db.query(DbPost).filter((DbPost.id == id) & (DbPost.user_id == user_id))

    post_data = post.first()

    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="post not found")

    # if post_data.user_id != user_id:
    #     raise unauthorized_exception
    
    post.update(
        {
        'image_url': request.image_url,
        'image_url_type':request.image_url_type,
        'caption': request.caption,
        'date_created':datetime.now(),
        }
    )
    
    db.commit()

    return post.first()

def get_all_posts(db: Session):
    return db.query(DbPost).all()