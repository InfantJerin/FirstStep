import langroid.language_models as lm
from langroid.pydantic_v1 import BaseModel
from typing import List, Dict
from datetime import datetime, timedelta
import vertexai
import os
import langroid as lr
from langroid.agent.tools.orchestration import DoneTool
from enum import Enum

vertexai.init(project="hack-poc-435717", location="us-east5")
os.environ['GOOGLE_CLOUD_PROJECT'] = 'hack-poc-435717'
os.environ['VERTEXAI_PROJECT'] = 'hack-poc-435717'  # Replace with your actual project ID
os.environ['VERTEXAI_LOCATION'] = 'us-east5'  
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'G:\projects\jerin\hack-poc-435717-c297a1387bf8.json'

llm_cfg = lm.OpenAIGPTConfig( # or OpenAIAssistant to use Assistant API 
  # any model served via an OpenAI-compatible API
  chat_model='litellm/gemini-1.5-pro', # or, e.g., "ollama/mistral"
)

config = lr.ChatAgentConfig(
        llm = llm_cfg
    )

peson_interest_prompt = """
        You are an AI assistant tasked with gathering information about a user through open-ended conversation. Your goal is to discover the user's interests, skills, motivations, business ideas, and potential employment opportunities.
        Engage in a natural conversation, asking relevant questions to gather this information. Once you have sufficient data, compile it into a JSON format with the following fields:
        - interests
        - skills
        - motivations
        - business_ideas
        - potential_employment
        Only end the conversation when you have gathered enough information to populate these fields. If you have the required information, respond with 'CONVERSATION_COMPLETE' followed by the JSON data.
        Start your conversation with a question to understand the user's interests. DO NOT respond smileys in your responses.
"""

peson_interest_test_prompt = """
        You are an AI assistant tasked with gathering information about a user through open-ended conversation. Your goal is to discover the user's interests, skills, motivations, business ideas, and potential employment opportunities.
        Engage in a natural conversation, asking relevant questions to gather this information. Once you have sufficient data, compile it into a JSON format with the following fields:
        - interests
        - skills
        - motivations
        - business_ideas
        - potential_employment
        Only end the conversation when you have gathered enough information to populate these fields. If you have the required information, present it with the `person_interests` tool/function.
        Start your conversation with a question to understand the user's interests. DO NOT respond smileys in your responses.
        For Demo purpose, end the conversation after 5 messages.
"""

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
    date_achieved: datetime = None

class ConversationSummary(BaseModel):
    date: datetime
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

person_info = PersonInfo(
    name="John Doe",
    age=30,
    gender="Male",
    location="New York",
    occupation="Software Engineer",
    person_interests=PersonInterestsData(
        interests=["Reading", "Traveling", "Cooking"],
        skills=["Python", "SQL", "Machine Learning"],
        motivations=["To make a positive impact", "To learn new things"],
        business_ideas=["Online Tutoring", "E-commerce"],
        potential_employment=["Google", "Facebook"]
    ),
    milestones=[
        Milestone(name=MilestoneEnum.FINDING_INTEREST, achieved=True, date_achieved=datetime.now()),
        Milestone(name=MilestoneEnum.LEARNING_FROM_COURSES, achieved=False),    
    ],
    conversation_summaries=[
        ConversationSummary(date=datetime.now() - timedelta(days=30), summary="Discussed interests and potential employment opportunities."),
        ConversationSummary(date=datetime.now() - timedelta(days=15), summary="Discussed business ideas and skills.")
        ]
)

personal_agent_prompt = f""" You are AI agent who is going to help the user in the journey of employment or bussiness.
There are 4 stages in the journey:
1. Finding Interest: The user is exploring their interests and skills.
2. Learning from Courses: The user is learning from courses to improve their skills.
3. Starting Business: The user is starting a business.
4. Eligible for Loan: The user is eligible for a loan.
user info and progress: {person_info}
You can use the <person_info_tool> tool to get the info about the user, it contains details about the user progress in the journey.
You can use the user info to guide him in the journey.
Be polite and helpful. Understand the user's preferences and guide him accordingly.
You are conversing with the user, so do not provide any bullet points or lists in your responses. becuase your responses will be a audio output. so keep it simple and short.
DO NOT USE SMILEYS IN YOUR RESPONSES.

"""


class PersonInfoTool(lr.agent.ToolMessage):
    """Tool to return the person info"""

    request: str = "person_info_tool"
    purpose: str = "Provide the person info for llm to have the context of the user"
    personInfo: PersonInfo = person_info

    def handle(self) -> str:
        """Tool handler: Print the info about the person.
        Any format errors are intercepted by Langroid and passed to the LLM to fix."""
        return f'You are given with the person info. Use it to remember the user context {self.personInfo}'


class PersonInterest(lr.agent.ToolMessage):
    """Tool to collect information about a user's interests, skills, motivations, business ideas, and potential employment opportunities."""

    request: str = "person_interests"
    purpose: str = "Collect the person interests <personInterestsData> from the given JSON response"
    personInterestsData: List[PersonInterestsData]

    def handle(self) -> str:
        """Tool handler: Print the info about the person interests.
        Any format errors are intercepted by Langroid and passed to the LLM to fix."""
        print(f"Correctly extracted Person Interests Info: {self.personInterestsData}")
        return "DONE"  # terminates task


interestFinderAgent = lr.ChatAgent(config)
interestFinderAgent.enable_message(PersonInterest)

person_interest_finder_task = lr.Task(interestFinderAgent, name="InterestFinder",
                        interactive= True,
                        system_message= peson_interest_test_prompt)

person_agent = lr.ChatAgent(config)
person_agent.enable_message(PersonInfoTool)
person_agent_task = lr.Task(person_agent, name="PersonAgent",
                        interactive= True,
                        system_message= personal_agent_prompt)

person_agent_task.run("Hello")


message_history = person_agent.message_history[1:]
current_message_history = [(i.role.value, i.content) for i in message_history]
print(current_message_history)

done_tool = DoneTool.default_value("request")

summary_agent = lr.ChatAgent(config)
summary_agent_task = lr.Task(summary_agent, name="SummaryAgent",
                        interactive= False,
                        system_message= f'''
                            You are going to summarize the current conversation history of the user.
                            Provide the summary in a single paragraph.
                            Output Format:
                            - date: <date>
                            - summary: <summary>

                           set the output using the TOOL: `{done_tool}` with `content`  field equal to a string.    
                        ''',
                        user_message= f'''Conversation history: {current_message_history}''')

summary_agent.enable_message(DoneTool)
result  = summary_agent_task.run()
print(result.content)
