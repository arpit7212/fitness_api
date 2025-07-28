from fastapi import FastAPI
from app.database import Base, engine
from app.routes import subjects, clients, bookings, slots


app = FastAPI(title="Fitness Studio API")

Base.metadata.create_all(bind=engine)



app.include_router(subjects.router)
app.include_router(clients.router)
app.include_router(bookings.router)
app.include_router(slots.router)