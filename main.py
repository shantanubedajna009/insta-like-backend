from fastapi import FastAPI
from database.db import engine
from database import models
from router.user import router as user_router
from router.post import router as post_router
from authentication.auth_routes import router as auth_router
from router.comment import router as comment_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)
app.include_router(comment_router)

@app.get('/')
def index():
    return "Index Page"

models.Base.metadata.create_all(engine)

# allow cros origin requests
# like from an react app
origins = [
  'http://localhost:3000'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ['*']
)   
                                                    # name is it refer to it in templates
app.mount('/images', StaticFiles(directory='images'), name='imageroute')