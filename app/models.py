from pydantic import BaseModel, Field
from typing import List, Optional
from enum import IntEnum

class Priority(IntEnum):
    EMERGENCY = 0      # Highest
    PAID_PRIORITY = 1
    FOLLOW_UP = 2
    ONLINE = 3
    WALK_IN = 4        # Lowest

class Token(BaseModel):
    token_id: str
    patient_name: str
    priority: Priority
    status: str = "pending"

class Slot(BaseModel):
    slot_id: str
    start_time: str
    end_time: str
    max_capacity: int
    tokens: List[Token] = []