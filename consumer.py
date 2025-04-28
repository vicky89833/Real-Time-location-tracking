import json
from confluent_kafka import Consumer, KafkaException
import socketio
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Socket.IO setup
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'location-consumers',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': 'false',
    'session.timeout.ms': 6000,
    'heartbeat.interval.ms': 2000
}

@app.get("/")
async def user_page(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")

async def consume_messages():
    consumer = None
    try:
        consumer = Consumer(conf)
        consumer.subscribe(['user-locations'])
        logger.info("Kafka consumer subscribed to user-locations")
        
        while True:
            try:
                msg = consumer.poll(1.0)
                if msg is None:
                    await asyncio.sleep(0.1)
                    continue
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        logger.info("Reached end of partition")
                    else:
                        logger.error(f"Consumer error: {msg.error()}")
                    continue
                
                try:
                    data = json.loads(msg.value().decode('utf-8'))
                    logger.info(f"Received message: {data}")
                    await sio.emit('location_update', data)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
            except Exception as e:
                logger.error(f"Error in consumer loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying
    except Exception as e:
        logger.error(f"Consumer setup failed: {e}")
    finally:
        if consumer:
            consumer.close()
            logger.info("Kafka consumer closed")

@app.on_event("startup")
async def startup_event():
    # Test Kafka connection
    try:
        test_consumer = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'test'})
        metadata = test_consumer.list_topics(timeout=10)
        logger.info(f"Connected to Kafka. Available topics: {metadata.topics}")
        test_consumer.close()
    except Exception as e:
        logger.error(f"Kafka connection test failed: {e}")
        return
    
    # Start consumer task
    asyncio.create_task(consume_messages())

if __name__ == "__main__":
    uvicorn.run(socket_app, host="0.0.0.0", port=8001, log_level="info")
