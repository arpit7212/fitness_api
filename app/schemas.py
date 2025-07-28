from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class SubjectCreate(BaseModel):
    name: str
    instructor: str
    timezone: Optional[str] = "UTC"  # Optional timezone with default


class SlotInfo(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    available_positions: int

class Subject(BaseModel):
    id: int
    name: str
    instructor: str
    timezone: str
    slots: List[SlotInfo] = []
    
    model_config = ConfigDict(from_attributes=True)

class ClientCreate(BaseModel):
    name: str

class Client(BaseModel):
    id: int
    name: str

    
    model_config = ConfigDict(from_attributes=True)

class SlotCreate(BaseModel):
    subject_id: int
    start_time: datetime
    end_time: datetime

class Slot(BaseModel):
    id: int
    subject_id: int
    start_time: datetime
    end_time: datetime

    model_config = ConfigDict(from_attributes=True)



class BookingCreate(BaseModel):
    client_id: int
    slot_id: int

class Booking(BaseModel):
    id: int
    client_id: int
    slot_id: int

    model_config = ConfigDict(from_attributes=True)