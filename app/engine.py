from typing import List, Dict, Optional
from .models import Token, Slot, Priority

class AllocationEngine:
    def __init__(self):
        # Dictionary to store slots per doctor: {doctor_id: [List of Slots]}
        self.doctor_schedules: Dict[str, List[Slot]] = {}

    def add_doctor(self, doctor_id: str, slots: List[Slot]):
        self.doctor_schedules[doctor_id] = slots

    def allocate_token(self, doctor_id: str, slot_id: str, patient_name: str, source: Priority) -> Token:
        schedule = self.doctor_schedules.get(doctor_id)
        if not schedule:
            raise ValueError("Doctor not found")

        # Find the specific slot
        slot = next((s for s in schedule if s.slot_id == slot_id), None)
        if not slot:
            raise ValueError("Slot not found")

        # Check Hard Limit (Emergencies bypass this)
        if len(slot.tokens) >= slot.max_capacity and source != Priority.EMERGENCY:
            raise Exception("Slot is at maximum capacity")

        new_token = Token(
            token_id=f"TKN-{len(slot.tokens) + 1}",
            patient_name=patient_name,
            priority=source
        )

        # Dynamic Reallocation / Prioritization
        slot.tokens.append(new_token)
        # Sort tokens based on Priority (0 is highest)
        slot.tokens.sort(key=lambda x: x.priority)
        
        return new_token

    def handle_cancellation(self, doctor_id: str, slot_id: str, token_id: str):
        """
        When a token is cancelled, the engine automatically leaves 
        room for the next highest priority patient.
        """
        schedule = self.doctor_schedules.get(doctor_id)
        slot = next((s for s in schedule if s.slot_id == slot_id), None)
        
        if slot:
            slot.tokens = [t for t in slot.tokens if t.token_id != token_id]
            # After removal, the remaining list is still sorted by priority

    def prevent_starvation(self, doctor_id: str, slot_id: str):
        """
        [Advanced Feature] 
        Checks if any Standard patients have been pushed too far back. 
        If so, bumps them to 'PAID_PRIORITY' to ensure fairness.
        """
        schedule = self.doctor_schedules.get(doctor_id)
        slot = next((s for s in schedule if s.slot_id == slot_id), None)
        
        if not slot or not slot.tokens:
            return

        # LOGIC: If the last patient is Standard/Walk-in and there are > 2 people ahead,
        # upgrade them to Paid Priority to give them a fighting chance.
        last_token = slot.tokens[-1]
        
        # Only upgrade if they are currently low priority (Standard or Walk-in)
        if last_token.priority > Priority.PAID_PRIORITY and len(slot.tokens) > 2:
            print(f"⚠️ Starvation Detected: Upgrading {last_token.patient_name} to PAID PRIORITY")
            last_token.priority = Priority.PAID_PRIORITY
            
            # Re-sort immediately to reflect the new status
            slot.tokens.sort(key=lambda x: x.priority)