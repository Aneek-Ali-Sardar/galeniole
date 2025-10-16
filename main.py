from config.db import db, test_connection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager
from routes.auth import auth_router
from fastapi.staticfiles import StaticFiles

# Lifespan context for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    await test_connection()
    yield
    # Runs on shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="frontend"), name="frontend")

# Include auth routes
app.include_router(auth_router)

# -----------------------------
# Patient Model
# -----------------------------
class Patient(BaseModel):
    id: int
    name: str
    age: int
    condition: str

# In-memory storage for now
patients: List[Patient] = []

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def home():
    return {"message": "Hello, FastAPI is working!"}

@app.get("/patients", response_model=List[Patient])
def get_patients():
    return patients

@app.post("/patients", response_model=Patient)
def add_patient(patient: Patient):
    patients.append(patient)
    return patient

@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    for p in patients:
        if p.id == patient_id:
            return p
    raise HTTPException(status_code=404, detail="Patient not found")

@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, updated: Patient):
    for i, p in enumerate(patients):
        if p.id == patient_id:
            patients[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    for i, p in enumerate(patients):
        if p.id == patient_id:
            patients.pop(i)
            return {"message": "Patient deleted successfully"}
    raise HTTPException(status_code=404, detail="Patient not found")