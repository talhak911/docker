from fastapi import FastAPI,Depends
from sqlmodel import SQLModel,Field,Session
from contextlib import asynccontextmanager
from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
from .cofig.db import create_db_and_tables,get_session
from typing import Union, Optional, Annotated,AsyncGenerator
import asyncio



class Todo1(SQLModel,table=True):
    id:int=Field(primary_key=True)
    contant:str=Field(index=True)


    

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    # loop.run_until_complete(consume_messages('todos', 'broker:19092'))
    # task = asyncio.create_task(consume_messages('todos', 'broker:19092'))
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

async def get_kafka_prodcer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
         yield producer
    finally:
         await producer.stop()

@app.get('/')
def home():
    return {"hello":"product"}

@app.post('/create_todo')
async def send_one(todo:Todo1,session:Annotated[Session,Depends(get_session)],producer:Annotated[AIOKafkaProducer,Depends(get_kafka_prodcer)]):

    return {"message":"success"}

@app.post("/create_todo")
def create_todo(todo:Todo1,session:Annotated[Session,Depends(get_session)]):
    return "ok"