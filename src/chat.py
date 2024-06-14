import os,sys
# Add the project root to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functools import lru_cache
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.messages import SystemMessage
import os, re, json, sys
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,)

from utils.logger import logging
from utils.exception import CustomException

logging.info('Packages are imported successfully')  


@lru_cache(maxsize=128, typed=False)
def chatInitialize():
    groq_key = os.environ.get("GROQ_KEY")
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0.9, model_name="Llama3-70b-8192", groq_api_key=groq_key)
    logging.info('Intialize LLM successfully')
    return chat


# Global variables
entities = ['product_category', 'gender', 'price']

memory_with_user = ConversationBufferMemory(memory_key="history", return_messages=True)

def chatter(user_message: str):
    global entities
    items = entities
    print(items)
    try:
        if user_message == "":
            logging.info('User message is empty')
            raise CustomException("User message is empty")
        system_message = '''
            You are a smart and freindly customer care agent
            Your primary goal is to build a friendly conversation cunningly to get all the required details step by step for a product recomendation for cosmetics products.
            Short and sweet conversation is better.
            Required details are about {items}.
            If there is no missing fields, just say 'Thank you'. Missing fields : {items}
            Do not provide recomendations based on your traning data and world's data.
            Do not provide any blah. blahs like your capabilities and limitations. Be a customer care agent
        '''.format(items=items)
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
            llm=chatInitialize(),
            verbose = True,
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
    
memory_of_entity = ConversationBufferMemory(memory_key="history", return_messages=True)

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
            If user is not specifyiny or concerning about the information, make it 'flag_2'.
            Carefully choose between 'flag_1' and 'flag_2'.
            Do not hesitate to update as 'flag_2' when user is rejecting them, when conversation happens.
            Do not hesitate to update product description as well.
            If user is upto another use case, update infromation respectively.
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
            llm=chatInitialize(),
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

def json_extractor(text: str):
    try:
        # Compile a regular expression pattern to match JSON objects
        json_pattern = re.compile(r'\{.*?\}', re.DOTALL)
        
        # Find all matches in the text
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
                logging.error(f"Error decoding JSON: {e}")

        # Return the last JSON object if the list is not empty
        if json_data:
            last_json_obj = json_data[-1]
            logging.info(f'Extracted JSON data: {last_json_obj}')
            return last_json_obj
        else:
            logging.info('No valid JSON data found')
            return None
    except Exception as e:
        logging.error(e)
        raise e  # Raise the exception without custom handling to avoid undefined variables

    
def entity_checker(item):
    null_entities = {}
    nulls = []
    if item['product_category'] == 'flag_1':
        null_entities['product_category'] = 'flag_1'
        nulls.append('product_category')
    if item['gender'] == 'flag_1':
        null_entities['gender'] = 'flag_1'
        nulls.append('gender')
    if item['price'] == 'flag_1':
        null_entities['price'] = 'flag_1'
        nulls.append('price')
    logging.info('Null entities: '+str(null_entities))
    logging.info('Entity checker completed successfully')
    global entities
    entities = nulls
    print(entities)
    return null_entities


