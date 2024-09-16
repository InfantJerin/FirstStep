from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain.llms import  Anthropic
from langchain_google_vertexai import ChatVertexAI, VertexAI

from langchain.tools import Tool
import json
import vertexai

vertexai.init(project="hack-poc-435717", location="us-east5")

def get_user_info():
    return Tool(
        name="GetUserInfo",
        func=lambda _: "This tool doesn't actually fetch data. It's a placeholder for the conversation.",
        description="Get user information through conversation"
    )

def create_agent(llm_choice):
    if llm_choice.lower() == 'vertexai':
        llm = VertexAI()
    elif llm_choice.lower() == 'claude':
        llm = Anthropic(model="claude-2")
    else:
        raise ValueError("Invalid LLM choice. Choose 'vertexai' or 'claude'.")

    memory = ConversationBufferMemory(memory_key="chat_history")
    tools = [get_user_info()]

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        prompt=initial_prompt
    )

initial_prompt = PromptTemplate(
    input_variables=["chat_history"],
    template="""
    You are an AI assistant tasked with gathering information about a user through open-ended conversation. Your goal is to discover the user's interests, skills, motivations, business ideas, and potential employment opportunities.

    Engage in a natural conversation, asking relevant questions to gather this information. Once you have sufficient data, compile it into a JSON format with the following fields:
    - interests
    - skills
    - motivations
    - business_ideas
    - potential_employment

    Only end the conversation when you have gathered enough information to populate these fields. If you have the required information, respond with 'CONVERSATION_COMPLETE' followed by the JSON data.

    Previous conversation:
    {chat_history}

    Human: Let's start our conversation.
    AI: Great! I'd love to learn more about you. To begin, could you tell me a bit about your interests? What kind of activities or subjects do you enjoy spending time on?
    """
)

def main():
    llm_choice = 'vertexai'
    agent = create_agent(llm_choice)
    
    user_input = "Let's start our conversation."
    while True:
        response = agent.invoke(input=user_input)
        print("AI:", response)
        
        if "CONVERSATION_COMPLETE" in response:
            json_data = response.split("CONVERSATION_COMPLETE")[1].strip()
            user_info = json.loads(json_data)
            print("\nUser Information:")
            print(json.dumps(user_info, indent=2))
            break
        
        user_input = input("Human: ")

if __name__ == "__main__":
    main()