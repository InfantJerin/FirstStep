from langchain.chains import (
    ConversationChain,
    LLMChain,
    RetrievalQA,
    SimpleSequentialChain,
)
from langchain.chains.summarize import load_summarize_chain
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_google_vertexai import ChatVertexAI, VertexAI, VertexAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import vertexai

#hack-poc-435717
vertexai.init(project="hack-poc-435717", location="us-east5")
# LLM model
llm = VertexAI(
    model_name="gemini-1.5-flash-001",
    verbose=True,
)

# Chat
chat = ChatVertexAI(model="gemini-1.5-pro")

# Embedding
embeddings = VertexAIEmbeddings("text-embedding-004")

# You'll be working with simple strings (that'll soon grow in complexity!)
my_text = "What day comes after Friday?"

response = llm.invoke(my_text)
print(response)