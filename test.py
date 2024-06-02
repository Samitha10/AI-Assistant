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

def chatter(user_message: str):
    system_message = '''
        You are a smart and freindly assistant.
        Your prmary goal is to build a friendly conversation to get all the required details stepby step for a product recomendation for cosmetics products.
        Short and sweet conversation is better.
        Required details are 'product category', 'gender', 'age' and 'price'.
        If user has provided them in chat history, rememeber them and use them.
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

def entity_extractor(user_message: str):
    system_message = '''
        You are a smart and freindly assistant.
        Extract the information product category, gender, age and price from the user message when conversation happens.
        If you got those information from previous chat history remember them and use them.
        If there is no information for a specific area, make it '1'.
        If user is not specifying relevant information, make it '2'.
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

def json_extractor(text:str):
    json_pattern = re.compile(r'\{.*?\}', re.DOTALL)
    json_matches = json_pattern.findall(text)

    # Initialize a list to hold the extracted JSON objects
    json_data = []

    # Parse each JSON section and add it to the list
    for match in json_matches:
        try:
            json_obj = json.loads(match)
            json_data.append(json_obj)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    # Print the extracted JSON data
    for item in json_data:
        return item
    
def entity_checker(item):
    null_entities = []

    if item['product_category'] == "1" or item['product_category'] == '2' :
        null_entities.append('product_category')
    if item['gender'] == '1' or item['gender'] == '2' :
        null_entities.append('gender')
    if item['age'] == '1' or item['age'] == '2' :
        null_entities.append('age')
    if item['price'] == '1' or item['price'] == '2':
        null_entities.append('price')

    return null_entities  # return list of entities if null values exist

def filter(item:list):
    if not item:
        return True
    else:
        return False


def recomendation_selector(products: dict, item:list):
    product_list=[]
    if filter(item) == True:
        if products['product_category'] != 'false' or products['product_category'] != 'False':
            product_list.append(products['product_category'])
        if products['gender'] != 'false' or products['gender'] != 'False':
            product_list.append(products['gender'])
        if products['age'] != 'false' or products['age'] != 'False':
            product_list.append(products['age'])
        if products['price'] != 'false' or products['price'] != 'False':
            product_list.append(products['price'])

        return product_list
    else:
        print("There are null entities in the item")
        return False


print(entity_extractor("my name is john"))
print(entity_extractor("my girlfriend is celebrating her 25th birthday"))
print(entity_extractor("she loves skin care products"))
a = entity_extractor("My budget is $300")
print(a)

b = json_extractor(a)

c = entity_checker(b)

lists = recomendation_selector(b, c)
print(lists)