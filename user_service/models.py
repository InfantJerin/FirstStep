from sqlalchemy import Column, Integer, String, Date, JSON, create_engine, Text, DateTime
from datetime import datetime, timedelta, timezone
from .database import Base

class PersonDetails(Base):
    __tablename__ = 'person_details'
    __table_args__ = {'schema': 'first_step'} 
    id = Column(Integer, primary_key=True, autoincrement=True)
    adhaar_number = Column(String, unique=True, nullable=False)
    person_info = Column(JSON, nullable=True)

class UserSessionMessages(Base):
    __tablename__ = 'user_session_messages'
    __table_args__ = {'schema': 'first_step'} 
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    session_date = Column(DateTime, default=datetime.now(timezone.utc)) 
    messages = Column(JSON, nullable=True)

class UserSessionSummary(Base):
    __tablename__ = 'user_session_summary'
    __table_args__ = {'schema': 'first_step'} 
    session_summary_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    summary_date = Column(DateTime, default=datetime.now(timezone.utc)) 