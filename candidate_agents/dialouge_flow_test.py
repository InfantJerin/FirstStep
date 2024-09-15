import os
import json
import requests

from langchain.chat_models import ChatOpenAI
from langchain.callbacks import CallbackManager, StreamingCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Replace with your Dialogflow API key and agent ID
DIALOGFLOW_API_KEY = "YOUR_API_KEY"
DIALOGFLOW_AGENT_ID = "YOUR_AGENT_ID"

def send_message_to_dialogflow(message):
    url = f"https://api.dialogflow.com/v2/projects/{DIALOGFLOW_AGENT_ID}/agent/sessions/{DIALOGFLOW_API_KEY}/detectIntent"

    headers = {
        "Authorization": f"Bearer {DIALOGFLOW_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "queryInput": {
            "text": {
                "text": message
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    return response_json["queryResult"]["fulfillmentText"]

def create_llm_chain():
    llm = ChatOpenAI(temperature=0.7)
    prompt_template = PromptTemplate(
        input_variables=["query"],
        template="Combine the following information to provide a comprehensive and informative response:\n\n**Query:** {query}\n\n**Additional Information:** {additional_info}"
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain

def main():
    callback_manager = CallbackManager()
    callback_manager.add_handler(StreamingCallbackHandler())

    llm_chain = create_llm_chain()

    while True:
        user_input = input("You: ")

        # Send the message to Dialogflow and get the response
        dialogflow_response = send_message_to_dialogflow(user_input)

        # Combine the user's input and Dialogflow's response as additional information
        additional_info = f"**User:** {user_input}\n**Dialogflow:** {dialogflow_response}"

        # Generate a response using LangChain
        response = llm_chain.run(query=user_input, additional_info=additional_info)

        print("AI Assistant:", response)

if __name__ == "__main__":
    main()