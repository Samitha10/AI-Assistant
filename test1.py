from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain,LLMChain
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

# Initialize the memory object
memory_with_user = ConversationBufferWindowMemory(k=5, memory_key="history", return_messages=True)

def chatter(user_message: str):
    system_message = '''
        You are a smart and freindly assistant.
        Your prmary goal is to build a friendly conversation to get all the required details stepby step for a product recomendation for cosmetics products.
        Short and sweet conversation is better.
        Required details are 'product category', 'gender', 'age' and 'price'.
    '''
    human_message = user_message

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_message),  # The persistent system prompt
            MessagesPlaceholder(variable_name="history"),  # The conversation history
            HumanMessagePromptTemplate.from_template("{input}"),  # The user's current input
        ]
    )

    # Create the conversation chain
    chain = ConversationChain(
        memory=memory_with_user,
        llm=chat,
        verbose=False,
        prompt=prompt,
    )

    # Predict the answer
    answer = chain.predict(input=human_message)
    
    # Save the context
    memory_with_user.save_context({"input": human_message}, {"output": answer})
    
    return answer

def memLoader():
    mem = memory_with_user.load_memory_variables({})
    return mem

def chat_interface():
    print(chatter("what is 10+15"))
    print(chatter("Then substract 5"))
    print(chatter("now devide by 2"))

chat_interface()
