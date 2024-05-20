from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
app = FastAPI()
@app.get('/')
def home():
    return {"hello":"ord"}

@app.post('/producer')
async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092', security_protocol='PLAINTEXT')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("order", b"Super message")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()
    return {"message":"success"}