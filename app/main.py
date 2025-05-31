from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import timedelta
from . import models, schemas, crud, auth, views_tracker
from .database import SessionLocal, engine
from datetime import datetime
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Content Management System",
    description="A RESTful API for managing articles with user authentication and view tracking",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/articles/", response_model=schemas.Article)
def create_article(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_user_article(db=db, article=article, user_id=current_user.id)

@app.get("/articles/", response_model=List[schemas.Article])
def read_articles(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    articles = crud.get_user_articles(db, user_id=current_user.id, skip=skip, limit=limit)
    return articles

@app.get("/articles/{article_id}", response_model=schemas.ArticleWithViews)
def read_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if db_article.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this article")
    
    # Track the view
    views_tracker.recent_views_tracker.track_view(current_user.id, article_id)
    crud.create_article_view(db, user_id=current_user.id, article_id=article_id)
    
    # Get view count and create response
    view_count = crud.get_article_view_count(db, article_id=article_id)
    
    # Create response with all required fields
    return {
        "id": db_article.id,
        "title": db_article.title,
        "content": db_article.content,
        "created_at": db_article.created_at,
        "updated_at": db_article.updated_at,
        "owner_id": db_article.owner_id,
        "view_count": view_count
    }

@app.put("/articles/{article_id}", response_model=schemas.Article)
def update_article(
    article_id: int,
    article: schemas.ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if db_article.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this article")
    
    updated_article = crud.update_article(db, article_id=article_id, article=article, user_id=current_user.id)
    return updated_article

@app.delete("/articles/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    success = crud.delete_article(db, article_id=article_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Article not found or not authorized")
    return {"message": "Article deleted successfully"}