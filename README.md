# JokeAPI

API for saving and editing jokes. 

### Used libraries

 - FastAPI
 - SQLAlchemy
 - passlib
 - requests
 - pydantic
---

### Description
#### Authentication 
HTTPBasic

| Security Scheme Type | HTTP Authotization Scheme |
--|--
| HTTP | basic |

---

#### Create New User
**POST** /users/
Request samples:
Content type: application/json
{
    "username": "string",
    "password": "string"
}

Response samples:
Content type: application/json
{
    "username": "string",
    "id": 0,
    "jokes": []
}

---

#### Get List Jokes
**GET** /jokes/
---

#### Create New Joke
**POST** /jokes/
Request sample:
{
    "text": "string" (optional)
}

Response sample:
{
    "text": "string",
    "id": 0,
    "owner_id": 0
}

---

#### Get Joke
**GET** /jokes/{joke_id}
Response sample:
{
    "text": "string",
    "id": 0,
    "owner_id": 0
}

---

#### Update Joke
**PUT** /jokes/{joke_id}
Request sample:
{
    "text": "string",
    "id": 0
}

Response sample:
{
    "text": "string",
    "id": 0,
    "owner_id": 0
}

---

#### Delete Joke
**DELETE** /jokes/{joke_id}
