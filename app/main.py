from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, transaction
from app.routes import auth, transaction as transaction_routes, dashboard

app = FastAPI(
    title="Finance Backend",
    description="Backend system for financial data processing and access control"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(transaction_routes.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    return {"message": "Finance Data Processing and Access Control Backend is running"}
