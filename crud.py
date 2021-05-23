from sqlalchemy.orm import Session
import requests
import models, schemas

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate, password: str):
    db_user = models.User(username=user.username, hashed_password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_jokes(db: Session, user: models.User):
    return db.query(models.Joke).filter(models.Joke.owner_id == user.id).all()

def get_joke(db: Session, joke_id: int):
    return db.query(models.Joke).filter(models.Joke.id == joke_id).first()

def create_user_joke(db: Session, joke: schemas.JokeCreate, user_id: int):
    if not joke.text:
        joke.text = requests.get("https://geek-jokes.sameerkumar.website/api").json()
    db_joke = models.Joke(**joke.dict(), owner_id=user_id)
    db.add(db_joke)
    db.commit()
    db.refresh(db_joke)
    return db_joke

def update_joke(db:Session, joke: schemas.JokeUpdate, db_joke: models.Joke):
    db_joke.text = joke.text
    db.commit()
    db.refresh(db_joke)
    return db_joke

def delete_joke(db: Session, joke_id: int):
    db.query(models.Joke).filter(models.Joke.id == joke_id).delete()
    db.commit()
    return []
