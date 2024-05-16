from typing import Annotated
from fastapi import FastAPI,Depends,HTTPException
from jose import JWTError,jwt
from datetime import datetime , timedelta
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
fake_users_db: dict[str, dict[str, str]] = {
    "talha": {
        "username": "talha",
        "full_name": "Muhammad Talha",
        "email": "talha@example.com",
        "password": "123",
    },
    "mjunaid": {
        "username": "mjunaid",
        "full_name": "Muhammad Junaid",
        "email": "mjunaid@example.com",
        "password": "mjunaidsecret",
    },
}

ALGORITHM = "HS256"
SECRET_KEY = "A Secure Secret Key"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def create_access_token(sub:str,expiry:timedelta)->str:
    expire=datetime.utcnow() + expiry
    to_encode = {"exp":expire,"sub":str(sub)}
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(access_token: str):
    decoded_jwt = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_jwt

app = FastAPI()

@app.post("/login")
def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends(OAuth2PasswordRequestForm)]):
    user_in_fake_db= fake_users_db.get(form_data.username)
    if not user_in_fake_db:
        raise HTTPException(status_code=400,detail="incorrect username")
    if not form_data.password == user_in_fake_db["password"]:
        raise HTTPException(status_code=400,detail="incorrect password")
    access_token_expires= timedelta(minutes=2)
    access_token = create_access_token(
        sub=user_in_fake_db["username"],expiry=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "expires_in": access_token_expires.total_seconds() }   

@app.get("/get-token")
def get_access_token(user_name: str):
    """
    Understanding the access token
    -> Takes user_name as input and returns access token
    -> timedelta(minutes=1) is used to set the expiry time of the access token to 1 minute
    """

    access_token_expires = timedelta(minutes=1)
    access_token = create_access_token(
        sub=user_name, expiry=access_token_expires)

    return {"access_token": access_token}

@app.get("/get_users")
def get_users(token: Annotated[str, Depends(oauth2_scheme)]):
    user_token_data = decode_access_token(token)
    
    user_in_db = fake_users_db.get(user_token_data["sub"])
    
    return user_in_db