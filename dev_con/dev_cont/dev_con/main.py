from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends
from sqlmodel import SQLModel,Field,Session,create_engine
import os
from dotenv import load_dotenv
load_dotenv()
from typing import AsyncGenerator,Annotated

class students(SQLModel,table = True):
    id:int =Field(primary_key=True)
    name:str


connection_string=os.getenv("DATABASE_URL")
engine =create_engine(connection_string)

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    yield

def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)

app = FastAPI(lifespan=lifespan,
              title="Hello World API with DB", 
    version="0.0.1",
    servers=[ 
        {
            "url": "http://0.0.0.0:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

def get_session():
    with Session(engine) as session:
        yield session


@app.get('/')
def get_students():
    return [{"name":"talha"}]

@app.post('./add_student')
def add_stuent(student:students,session:Annotated[Session,Depends(get_session)])->students:
    session.add(student)
    session.commit()
    session.refresh(student)
    return student