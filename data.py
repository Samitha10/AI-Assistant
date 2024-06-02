from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_core.messages import SystemMessage
import os, re, json
import streamlit as st
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,)


# Ensure you have the correct environment variable set
groq_key = os.environ.get("GROQ_KEY")

# Initialize the ChatGroq model
chat = ChatGroq(temperature=0.7, model_name="Llama3-70b-8192", groq_api_key=groq_key)

from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

import pandas as pd

df = pd.read_csv(
    "product_details.csv"
)
agent = create_pandas_dataframe_agent(chat, df, verbose=True)

answer = agent.invoke('give me a list of in stock products price under $15')
print(answer)