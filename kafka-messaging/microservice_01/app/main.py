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

async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-todos-group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

    

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    # loop.run_until_complete(consume_messages('todos', 'broker:19092'))
    # task = asyncio.create_task(consume_messages('todos', 'broker:19092'))
    create_db_and_tables()
    task = asyncio.create_task(consume_messages('my_todo', 'broker:19092'))
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
    todo_json = todo.model_dump_json().encode("utf-8")
    await producer.send_and_wait("my_todo", todo_json)
    return {"message": "success"}
 

@app.post("/create_todo")
def create_todo(todo:Todo1,session:Annotated[Session,Depends(get_session)]):
    return "ok"