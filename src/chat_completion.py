from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_core.messages import SystemMessage
import os, re, json, sys
import streamlit as st
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,)

from product_search import similarity_search
from image_retriver import image_tracker

# Add the project root to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
    try:
        if user_message == "":
            logging.info('User message is empty')
            raise CustomException("User message is empty")
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
        logging.info(f'User message: {user_message}, Answer: {answer}')
        logging.info('Chatter completed successfully')
        return answer
    except Exception as e:
        logging.info(e)
        raise CustomException(e,sys)

def entity_extractor(user_message: str):
    try:
        if user_message ==  "":
            logging.info('User message is empty')
            raise CustomException("User message is empty")
        system_message = '''
            You are a smart assistant.
            Extract the information 'product_category : string', 'gender: string', 'price: integer' from the user message when conversation happens.
            If there is some information about the product, add 'product_description: string' in the answer
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
        logging.info(f'User message: {user_message}, Answer: {answer}')
        logging.info('Entity extractor completed successfully')
        return answer
    except Exception as e:
        logging.info(e)
        raise CustomException(e, sys)

def json_extractor(text:str):
    try:
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
        logging.info(f'Extracted JSON data: {json_data}')
    except Exception as e:
        logging.info(e)
        raise CustomException(e,sys)
    
def entity_checker(item):
    null_entities = {}
    if item['product_category'] == 'flag_1':
        null_entities['product_category'] = 'flag_1'
    if item['gender'] == 'flag_1':
        null_entities['gender'] = 'flag_1'
    if item['price'] == 'flag_1':
        null_entities['price'] = 'flag_1'
    logging.info('Null entities: ', null_entities)
    logging.info('Entity checker completed successfully')
    return null_entities

def filter(item:dict):
    if len(item) == 0:
        return True
    else:
        return False


def recomendation_selector(products: dict, item:dict):
    info_dict={}
    if filter(item) == True:
        if products['product_category'] != 'flag_1' :
            info_dict['product_category'] = products['product_category']
        if products['gender'] != 'flag_1':
            info_dict['gender'] = products['gender']
        if products['price'] != 'flag_1':
            info_dict['price'] = products['price']
        if products['product_description'] != 'flag_1':
            info_dict['product_description'] = products['product_description']
        logging.info('Recomendation selector: ', info_dict)
        logging.info('Recomendation selector completed successfully')
        return info_dict
    else:
        print("There are null entities in the item")
        logging.info('There are null entities in the item')
        return False

def recomender(products: dict):
    try:
        category = products['product_category']
        gender = products['gender']
        price = products['price']
        
        # Perform the search based on the extracted information
        results = similarity_search(category,'category' )
        output = []
        for doc, score in results:
            output.append({doc.metadata['id']})
        output = [item for sublist in output for item in sublist]
        print(output)
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