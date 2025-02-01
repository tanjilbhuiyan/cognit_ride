import asyncio

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.event_recievers.recieve_passanger_added_event import consume_passenger_events
from app.event_recievers.recieve_rider_added_event import consume_rider_events
from app.repository.database import db
from app.tests.events_tester import publish_message

# from app.controller.PaymentAccount.payment_account import router as payment_account_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Create database tables on application startup
#     db.connect()
#     yield
#     # Clean up resources on application shutdown
#     db.close()


app = FastAPI(
    title="A.Xpress",
    docs_url="/api/docs",
    debug=True,
    # lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware, allow_headers=["*"], allow_origins=["*"], allow_methods=["*"]
)


# app.include_router(payment_account_router, prefix="/api/v1")


async def run_consumer_in_background():
    loop = asyncio.get_event_loop()

    # Run both tasks concurrently
    task1 = loop.run_in_executor(None, consume_passenger_events)
    task2 = loop.run_in_executor(None, consume_rider_events)

    # Wait for both tasks to complete (they won't, since they run forever)
    await asyncio.gather(task1, task2)


@app.on_event("startup")
async def startup_event():
    # Schedule the background tasks to run concurrently
    asyncio.create_task(run_consumer_in_background())


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        reload=True,
        port=8889,
    )
