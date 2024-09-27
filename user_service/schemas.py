from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum



class PersonInterestsData(BaseModel):
    interests: List[str]
    skills: List[str]
    motivations: List[str]
    business_ideas: List[str]
    potential_employment: List[str]

class MilestoneEnum(str, Enum):
    FINDING_INTEREST = "finding_interest"
    LEARNING_FROM_COURSES = "learning_from_courses"
    STARTING_BUSINESS = "starting_business"
    ELIGIBLE_FOR_LOAN = "eligible_for_loan"

class Milestone(BaseModel):
    name: MilestoneEnum
    achieved: bool
    date_achieved: Optional[datetime] = None 

class ConversationSummary(BaseModel):
    date: Optional[datetime] = None 
    summary: str

class PersonInfo(BaseModel):
    name: str
    age: int
    gender: str
    location: str
    occupation: str
    person_interests: PersonInterestsData
    milestones: List[Milestone]
    conversation_summaries: List[ConversationSummary]

class PersonDetailsModel(BaseModel):
    id: int
    adhaar_number: str
    person_info: Optional[PersonInfo]  # Use Optional if it can be None

    class Config:
        from_attributes = True  # Allows compatibility with SQLAlchemy models
