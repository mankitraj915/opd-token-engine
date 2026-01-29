from fastapi import FastAPI, HTTPException
from typing import List
from .models import Slot, Priority, Token
from .engine import AllocationEngine

app = FastAPI(title="OPD Token Allocation Engine")
engine = AllocationEngine()

@app.post("/setup-doctor/{doctor_id}")
async def setup_doctor(doctor_id: str, slots: List[Slot]):
    engine.add_doctor(doctor_id, slots)
    return {"status": "success", "message": f"Schedule for {doctor_id} initialized"}

@app.post("/book-token/{doctor_id}/{slot_id}")
async def book_token(doctor_id: str, slot_id: str, name: str, priority: Priority):
    try:
        return engine.allocate_token(doctor_id, slot_id, name, priority)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))