from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.Database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(String, primary_key=True)
    company_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    location = Column(String)
    date_applied = Column(Date)
    source = Column(String)
    status = Column(String)  # Applied, Interview, Offer, etc.
    salary_expectation = Column(String)
    notes = Column(Text)
    resume_file = Column(String)
    cover_letter_file = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    status_history = relationship("StatusHistory", back_populates="application", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="application", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="application", cascade="all, delete-orphan")

    @property
    def formatted_date(self):
        return self.date_applied.strftime("%d-%m-%Y") if self.date_applied else ""

class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True)
    application_id = Column(String, ForeignKey("applications.id"))
    old_status = Column(String)
    new_status = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

    application = relationship("Application", back_populates="status_history")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    application_id = Column(String, ForeignKey("applications.id"))
    name = Column(String)
    role = Column(String)
    email = Column(String)
    phone = Column(String)
    notes = Column(Text)

    application = relationship("Application", back_populates="contacts")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    application_id = Column(String, ForeignKey("applications.id"))
    remind_at = Column(DateTime)
    message = Column(Text)
    done = Column(Boolean, default=False)

    application = relationship("Application", back_populates="reminders")
