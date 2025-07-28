# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    instructor = Column(String, index=True)
    timezone = Column(String, default="UTC")  # Store the subject's timezone
    
    slots = relationship("Slot", back_populates="subject")  # One-to-many relationship with slots


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    bookings = relationship("Booking", back_populates="client")  # One-to-many relationship with bookings


class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))  # Foreign key to Subject
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime)

    subject = relationship("Subject", back_populates="slots")  # Reference to Subject
    bookings = relationship("Booking", back_populates="slot")  # One-to-many relationship with bookings


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))  # Foreign key to Client
    slot_id = Column(Integer, ForeignKey("slots.id"))  # Foreign key to Slot

    client = relationship("Client", back_populates="bookings")  # Reference to client
    slot = relationship("Slot", back_populates="bookings")  # Reference to Slot

    # Prevent the same student from booking the same slot multiple times
    __table_args__ = (
        UniqueConstraint("client_id", "slot_id", name="unique_booking"),
    )