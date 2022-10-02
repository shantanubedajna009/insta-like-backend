import datetime
from typing import List
from pydantic import BaseModel
from enum import Enum


class UrlType(str, Enum):
    short= 'absolute'
    story= 'relative'


####### Reveiver Schemas ############################

class UserRequest(BaseModel):
    username: str
    email: str
    password: str

class PostRequest(BaseModel):
    image_url: str
    image_url_type: UrlType
    caption: str

class UserAuth(BaseModel):
  id: int
  username: str
  email: str

class CommentRequest(BaseModel):
    content: str
    post_id: int

class CommentRequestForUpdate(BaseModel):
    content: str

######## Receiver Schemas ends here #################

############ Display Schemas ########################

class UserDisplay(BaseModel):
    username: str
    email: str
    date_created: datetime.datetime

    class Config():
        orm_mode = True

class UserInsidePost(BaseModel):
    username: str

    class Config():
        orm_mode = True

class CommentDisplay(BaseModel):
    id: int
    content: str
    username: str
    timestamp: datetime.datetime

    class Config():
        orm_mode = True

class PostDisplaySchema(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    date_created: datetime.datetime

    user: UserInsidePost

    comments: List[CommentDisplay]

    class Config():
        orm_mode = True

########### Display Schemas ends here ###############