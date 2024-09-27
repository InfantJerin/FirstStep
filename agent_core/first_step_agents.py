
import langroid.language_models as lm
from langroid.pydantic_v1 import BaseModel
from typing import List
import vertexai
import os
import langroid as lr

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

person_interest_finder_task.run("Hello")
