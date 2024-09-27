from rich import print
from langroid.pydantic_v1 import BaseModel
from typing import List
import langroid as lr

import langroid.language_models as lm
import os
import vertexai

vertexai.init(project="hack-poc-435717", location="us-east5")
os.environ['GOOGLE_CLOUD_PROJECT'] = 'hack-poc-435717'
os.environ['VERTEXAI_PROJECT'] = 'hack-poc-435717'  # Replace with your actual project ID
os.environ['VERTEXAI_LOCATION'] = 'us-east5'  
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'G:\projects\jerin\hack-poc-435717-c297a1387bf8.json'

llm_cfg = lm.OpenAIGPTConfig( # or OpenAIAssistant to use Assistant API 
  # any model served via an OpenAI-compatible API
  chat_model='litellm/gemini-1.5-pro', # or, e.g., "ollama/mistral"
)


class City(BaseModel):
    name: str
    country: str
    population: int


class CitiesData(BaseModel):
    cities: List[City]


PASSAGE = """
Berlin is the capital of Germany. It has a population of 3,850,809. 
Paris, France's capital, has 2.161 million residents. 
Lisbon is the capital and the largest city of Portugal with the population of 504,718.
"""


class CitiesMessage(lr.agent.ToolMessage):
    """Tool/function to use to extract/present structured capitals info"""

    request: str = "capital_info"
    purpose: str = "Collect information about city <capitals> from a passage"
    capitals: List[CitiesData]

    def handle(self) -> str:
        """Tool handler: Print the info about the capitals.
        Any format errors are intercepted by Langroid and passed to the LLM to fix."""
        print(f"Correctly extracted Capitals Info: {self.capitals}")
        return "DONE"  # terminates task


agent = lr.ChatAgent(
    lr.ChatAgentConfig(
        name="CitiesExtractor",
        use_functions_api=True,
        use_tools=False,
        system_message=f"""
        From the passage below, extract info about city capitals, and present it 
        using the `capital_info` tool/function.
        PASSAGE: {PASSAGE}
        """,
        llm=llm_cfg
    )
)
# connect the Tool to the Agent, so it can use it to present extracted info
agent.enable_message(CitiesMessage)

# wrap the agent in a task and run it
task = lr.Task(
    agent,
    interactive=False,
)

task.run('hello')