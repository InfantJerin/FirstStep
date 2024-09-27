from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from typing import cast
from langchain_google_vertexai import ChatVertexAI, VertexAI
import os
import langroid.language_models as lm
import langroid as lr
import nest_asyncio

import vertexai

import chainlit as cl

vertexai.init(project="hack-poc-435717", location="us-east5")
os.environ['GOOGLE_CLOUD_PROJECT'] = 'hack-poc-435717'
os.environ['VERTEXAI_PROJECT'] = 'hack-poc-435717'  # Replace with your actual project ID
os.environ['VERTEXAI_LOCATION'] = 'us-east5'  
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'G:\projects\jerin\hack-poc-435717-c297a1387bf8.json'

llm_cfg = lm.OpenAIGPTConfig( # or OpenAIAssistant to use Assistant API 
  # any model served via an OpenAI-compatible API
  chat_model='litellm/gemini-1.5-pro', # or, e.g., "ollama/mistral"
)

nest_asyncio.apply()

@cl.on_chat_start
async def on_chat_start():

    config = lr.ChatAgentConfig(
        llm = llm_cfg
    )
    agent = lr.ChatAgent(config)
    agent_task = lr.Task(agent, name="InterestFinder",
                         interactive= True,
                         system_message= """
            You are an AI assistant tasked with gathering information about a user through open-ended conversation. Your goal is to discover the user's interests, skills, motivations, business ideas, and potential employment opportunities.

            Engage in a natural conversation, asking relevant questions to gather this information. Once you have sufficient data, compile it into a JSON format with the following fields:
            - interests
            - skills
            - motivations
            - business_ideas
            - potential_employment

            Only end the conversation when you have gathered enough information to populate these fields. If you have the required information, respond with 'CONVERSATION_COMPLETE' followed by the JSON data.

            Start your conversation with a question to understand the user's interests. DO NOT respond smileys in your responses.
    """)

   
    cl.user_session.set("agent_task", agent_task)


@cl.on_message
async def on_message(message: cl.Message):

    task: lr.Task = cast(lr.Task, cl.user_session.get("agent_task"))
    msg = cl.Message(content="Test")
    #await task.run_async(message.content)
    #await msg.send()
    lr.ChainlitTaskCallbacks(task, message)
    await task.run_async(message.content)
