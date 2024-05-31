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

# Initialize the memory object
memory_with_user = ConversationBufferWindowMemory(k=5, memory_key="history", return_messages=True)
memory_of_entity = ConversationBufferWindowMemory(k=5, memory_key="history", return_messages=True)


def entity_extractor(user_message: str):
    system_message = '''
        You are a smart and freindly assistant.
        Extract the information product category, gender, age and price from the user message when conversation happens.
        If you got those information from previous chat history remember them and use them.
        If there is no information for a specific area, make it 'null'.
        If user is not specifying relevant information, make it 'false'.
        Answer must include JSON formated information.
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
        memory=memory_of_entity,
        llm=chat,
        verbose=False,
        prompt=prompt,
    )

    # Predict the answer
    answer = chain.predict(input=human_message)
    
    # Save the context
    memory_with_user.save_context({"input": human_message}, {"output": answer})
    
    return answer

print(entity_extractor("my sister is celebrating her 25th birthday"))
print(entity_extractor("she loves skin care products"))
print(entity_extractor("i have 300 dollars now"))

