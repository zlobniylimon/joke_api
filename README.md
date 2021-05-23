# JokeAPI

API for saving and editing jokes. 

## Used libraries

 - FastAPI
 - SQLAlchemy
 - passlib
 - requests
 - pydantic


## Authentication 
HTTPBasic

| Security Scheme Type | HTTP Authotization Scheme |
--|--
| HTTP | basic |


## Create New User
Send username and password for registration.
**POST** /users/
Request samples:
Content type: application/json
```
{
    "username": "string",
    "password": "string"
}
```

Response samples:
Content type: application/json
```
{
    "username": "string",
    "id": 0,
    "jokes": []
}
```
Requests must contain header ```Authentication: Basic <credentials>```, where credentials is the Base64 encoding of ID and password joined by a single colon : (like this ```username:password```)

## Get List Jokes
Get list of your jokes
**GET**: /jokes/


## Create New Joke
Create new joke. If text is not sent, joke will be taken from [Geek Joke API](https://geek-jokes.sameerkumar.website/api).
**POST** /jokes/
Request sample:
```
{
    "text": "string" (optional)
}
```

Response sample:
```
{
    "text": "string",
    "id": 0,
    "owner_id": 0
}
```


## Get Joke
Get joke by id. Can't get joke from another user.
**GET** /jokes/{joke_id}
Response sample:
```
{
    "text": "string",
    "id": 0,
    "owner_id": 0
}
```


## Update Joke
Update existing joke. Text and id of the joke must be sent.
**PUT** /jokes/{joke_id}
Request sample:
```
{
    "text": "string",
    "id": 0
}
```
Response sample:
```
{
    "text": "string",
    "id": 0,
    "owner_id": 0
}
```


## Delete Joke
Delete your joke.
**DELETE** /jokes/{joke_id}
