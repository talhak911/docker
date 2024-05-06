from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel,Field,Session,create_engine,select
from dev_con.config.db import engine

from typing import AsyncGenerator

class students(SQLModel,table = True):
    id:int =Field(primary_key=True)
    name:str



@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    yield

def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)

app = FastAPI(lifespan=lifespan,
              title="Hello World API with DB", 
   )

def get_session():
    with Session(engine) as session:
        yield session


@app.get('/')
def get_students():
    with Session(engine) as session:
        stu=session.exec(select(students)).all()
        return stu

@app.post('/add_student')
def add_stuent(student:students):
  with Session(engine) as session:  
    session.add(student)
    session.commit()
    session.refresh(student)
    return {"message":"added successfully"}