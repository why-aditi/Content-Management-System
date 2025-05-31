from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas, auth
from datetime import datetime

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_user_articles(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Article)\
        .filter(models.Article.owner_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def create_user_article(db: Session, article: schemas.ArticleCreate, user_id: int):
    db_article = models.Article(**article.dict(), owner_id=user_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def update_article(db: Session, article_id: int, article: schemas.ArticleUpdate, user_id: int):
    db_article = get_article(db, article_id)
    if not db_article or db_article.owner_id != user_id:
        return None
    
    update_data = article.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_article, field, value)
    
    db_article.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: int, user_id: int):
    db_article = get_article(db, article_id)
    if not db_article or db_article.owner_id != user_id:
        return False
    
    db.delete(db_article)
    db.commit()
    return True

def create_article_view(db: Session, user_id: int, article_id: int):
    db_view = models.ArticleView(user_id=user_id, article_id=article_id)
    db.add(db_view)
    db.commit()
    return db_view

def get_article_view_count(db: Session, article_id: int):
    return db.query(func.count(models.ArticleView.id))\
        .filter(models.ArticleView.article_id == article_id)\
        .scalar()