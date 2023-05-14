from fastapi import FastAPI
from backend.app.api.routers import users, campaigns
from backend.app.api.db import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the routers
app.include_router(users.router)
app.include_router(campaigns.router)

