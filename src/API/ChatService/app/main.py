import asyncio
import json
from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from confluent_kafka import Producer, Consumer

from app.api.v1.api_router import router as v1_router
from app.config import settings
from app.db.session import sessionmanager

from app.core.state import connections


# -------------------- Lifespan (startup/shutdown) --------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Setup Kafka Producer ---
    producer_conf = {"bootstrap.servers": settings.KAFKA_BOOTSTRAP}
    producer = Producer(producer_conf)
    app.state.kafka_producer = producer

    # --- Setup Kafka Consumer ---
    consumer_conf = {
        "bootstrap.servers": settings.KAFKA_BOOTSTRAP,
        "group.id": "chat-group",
        "enable.auto.commit": False,
        "auto.offset.reset": "earliest",
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([settings.KAFKA_TOPIC])
    app.state.kafka_consumer = consumer

    # --- Setup shared connections dict ---
    app.state.connections = {}  # key: "user_id:chat_thread_id" -> list[asyncio.Queue]

    # Start background task for consuming messages
    loop = asyncio.get_event_loop()
    consumer_task = loop.create_task(_consume_kafka_loop(app))

    try:
        yield
    finally:
        # --- Shutdown ---
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass

        consumer.close()
        producer.flush(5.0)
        if sessionmanager._engine is not None:
            await sessionmanager.close()


# -------------------- Kafka Background Loop --------------------
async def _consume_kafka_loop(app: FastAPI):
    consumer: Consumer = app.state.kafka_consumer
    loop = asyncio.get_event_loop()

    while True:
        msg = await loop.run_in_executor(None, consumer.poll, 1.0)
        if msg is None:
            await asyncio.sleep(0.05)
            continue
        if msg.error():
            print("Kafka consumer error:", msg.error())
            continue

        try:
            payload = msg.value()
            if not payload:
                print("<Note Payload _consume_kafka_loop>")
                continue
            print("<Load message from kafka _consume_kafka_loop>")
            data = json.loads(payload.decode("utf-8"))
        except Exception as e:
            print("Kafka message parse error:", e)
            continue

        # Determine recipient queue(s)
        key = f"{data['user_id']}:{data['chat_thread_id']}"
        if key in connections:
            for queue in connections[key]:
                await queue.put((data, msg))  # include Kafka message for commit


# Initialize FastAPI app with lifespan
app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Include all API routes from v1 router
app.include_router(v1_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=5001)
