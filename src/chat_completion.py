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

from src.product_search import similarity_search
from src.image_retriver import image_tracker
from utils.logger import logging
from utils.exception import CustomException

logging.info('Packages are imported successfully')  

# Ensure you have the correct environment variable set
groq_key = os.environ.get("GROQ_KEY")
# Initialize the ChatGroq model
chat = ChatGroq(temperature=0.7, model_name="Llama3-70b-8192", groq_api_key=groq_key)

logging.info('Intialize LLM successfully')

# Initialize the memory object
memory_with_user = ConversationBufferWindowMemory(k=5, memory_key="history", return_messages=True)
memory_of_entity = ConversationBufferWindowMemory(k=5, memory_key="history", return_messages=True)

def chatter(user_message: str):
    system_message = '''
        You are a smart and freindly assistant.
        Your primary goal is to build a friendly conversation to get all the required details stepby step for a product recomendation for cosmetics products.
        Short and sweet conversation is better.
        Required details are 'product_category', 'gender', 'price'.
        If your goal is complete, just say 'Thank you'
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
        You are a smart assistant.
        Extract the information 'product_category : string', 'gender: string', 'price: integer' from the user message when conversation happens.
        If you got those information from previous chat history remember them and use them.
        If there is no information for a specific area yet, make it 'flag_1'.
        If user is not specifying relevant information for the area, make it 'flag_2'.
        Answer must include JSON formated information. Do not provide additional content in the answer
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
    memory_of_entity.save_context({"input": human_message}, {"output": answer})

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
    if item['product_category'] == 'flag_1':
        null_entities.append('product_category')
    
    if item['gender'] == 'flag_1':
        null_entities.append('gender')
    if item['price'] == 'flag_1':
        null_entities.append('price')
    return null_entities

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
        if products['price'] != 'false' or products['price'] != 'False':
            product_list.append(products['price'])

        return product_list
    else:
        print("There are null entities in the item")
        return False

def recomender(products: list):
    try:
        category = products[0]
        gender = products[1]
        price = products[2]
        
        # Perform the search based on the extracted information
        results = similarity_search(category,'category' )
        output = []
        for doc, score in results:
            output.append({doc.metadata['id']})
        output = [item for sublist in output for item in sublist]
        return output
        
    except Exception as e:
        print(e)
        return False

def main():
    st.subheader("Spa Cylone", divider="rainbow", anchor=False)
    st.sidebar.title("Output")

    
        # Initialize chat history if not already done
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatter" not in st.session_state:
        st.session_state.chatter = chatter
    if "entity_extractor" not in st.session_state:
        st.session_state.entity_extractor = entity_extractor

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        avatar = "🤖" if message["role"] == "assistant" else "👨‍💻"
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])
    
    prompt = st.chat_input("Enter your prompt here...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👨‍💻"):
                st.markdown(prompt)
        response = st.session_state.chatter(prompt)

        # Add the responses to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant", avatar="🤖"):
            st.write(response)

        st.sidebar.markdown('## entity extractor')
        a = st.session_state.entity_extractor(prompt)
        st.sidebar.write(a)
        st.sidebar.markdown('## json extractor')
        b = json_extractor(a)
        st.sidebar.write(b)
        st.sidebar.markdown('## entity checker')
        c = entity_checker(b)
        st.sidebar.write(c)
        st.sidebar.markdown('## recomendation selector')
        d = recomendation_selector(b, c)
        st.sidebar.write(d)
        if d != False:
            st.sidebar.markdown('## recomender')
            e = recomender(d)
            st.sidebar.write(e)
            image_list, url_list = image_tracker(e)
            # image_paths = ['product_images/' + name for name in image_list]
            # st.sidebar.image(image_paths)
            st.sidebar.markdown('## URL list')
            st.sidebar.write(url_list)



main()