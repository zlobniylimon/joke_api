from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from passlib.context import CryptContext

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["sha256_crypt"])

app = FastAPI()

security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def is_user(credentials: HTTPBasicCredentials = Depends(security), db: Session=Depends(get_db)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Basic"}
            )
    user = crud.get_user(db=db, username=credentials.username)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise exception
    return user

def joke_owner(joke: models.Joke, user: models.User):
    if joke.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return joke
        
@app.post("/users/", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user, password=get_password_hash(user.password))

@app.post("/jokes/", response_model=schemas.Joke)
def create_new_joke(joke: schemas.JokeCreate, db: Session=Depends(get_db), user: models.User=Depends(is_user)):
    db_joke = crud.create_user_joke(db=db, joke=joke, user_id=user.id )
    return db_joke

@app.get("/jokes/")
def get_list_jokes(db: Session=Depends(get_db), user: models.User=Depends(is_user)):
    return crud.get_jokes(db=db, user=user)

@app.get("/jokes/{joke_id}", response_model=schemas.Joke)
def get_joke(joke_id: int, db: Session=Depends(get_db), user: models.User=Depends(is_user)):
    db_joke = crud.get_joke(db=db, joke_id=joke_id)
    if not db_joke:
        raise HTTPException(status_code=404, detail="Not exist")
    return joke_owner(db_joke, user)

@app.put("/jokes/{joke_id}", response_model=schemas.Joke)
def update_joke(joke_id: int, joke: schemas.JokeUpdate, db: Session=Depends(get_db), user: models.User=Depends(is_user)):
    db_joke = crud.get_joke(db=db, joke_id=joke_id)
    if not db_joke:
        raise HTTPException(status_code=404, detail="Not exist")
    joke_owner(db_joke, user)
    return crud.update_joke(db, joke, db_joke)
    
    
@app.delete("/jokes/{joke_id}", status_code=204)
def delete_joke(joke_id: int, db: Session=Depends(get_db), user: models.User=Depends(is_user)):
    db_joke = crud.get_joke(db=db, joke_id=joke_id)
    if not db_joke:
        raise HTTPException(status_code=404, detail="Not exist")
    joke_owner(db_joke, user)
    return crud.delete_joke(db, joke_id)
