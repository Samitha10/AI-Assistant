import os,sys
# Add the project root to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import logging
from utils.exception import CustomException
import pandas as pd
from src.cases import case_1,case_2,case_3,case_4,case_5,case_6,case_7,case_8,case_9,case_10,case_11,case_12,case_13,case_14,case_15,case_16
from src.data_processor import data_file_importer

data = data_file_importer()

def chatCompletionChecker(sentence):
    sentence = sentence.lower()
    if 'thank you' in sentence or 'thanks' in sentence or 'thank' in sentence or 'thankyou' in sentence or 'thanksyou' in sentence:
        return True
    else:
        return False
def nameExtractor(item:list):
    df = data
    names = []
    for id in item:
        name = df[df['id'] == id]['product_name'].values[0]
        names.append(name)
    return names


def filters(item:dict):
    if len(item) == 0:
        return True
    else:
        return False
    
    
def recomendation_selector(products: dict, item:dict):
    info_dict={}
    if filters(item) == True:
        if products['product_category'] != 'flag_1' and products['product_category'] != 'flag_2':
            info_dict['product_category'] = products['product_category']
        if products['gender'] != 'flag_1' and products['gender'] != 'flag_2':
            info_dict['gender'] = products['gender']
        if products['price'] != 'flag_1' and products['price'] != 'flag_2':
            info_dict['price'] = products['price']
        if 'product_description' in products and products['product_description'] not in ['flag_1', 'flag_2']:
            info_dict['product_description'] = products['product_description']
        logging.info(info_dict)
        logging.info('Recomendation selector completed successfully')
        return info_dict
    else:
        print("There are null entities in the item")
        logging.info('There are null entities in the item')
        return False


def case_checker(item:dict):
    if 'product_category' in item and 'price' in item and 'gender' in item and 'product_description' in item:
        return 1
    # Three-element subsets
    if 'product_category' in item and 'price' in item and 'gender' in item:
        return 2
    if 'product_category' in item and 'price' in item and 'product_description' in item:
        return 3
    if 'product_category' in item and 'gender' in item and 'product_description' in item:
        return 4
    if 'price' in item and 'gender' in item and 'product_description' in item:
        return 5
    
    # Two-element subsets
    if 'product_category' in item and 'price' in item:
        return 6
    if 'product_category' in item and 'gender' in item:
        return 7
    if 'product_category' in item and 'product_description' in item:
        return 8
    if 'price' in item and 'gender' in item:
        return 9
    if 'price' in item and 'product_description' in item:
        return 10
    if 'gender' in item and 'product_description' in item:
        return 11
    
    # One-element subsets
    if 'product_category' in item:
        return 12
    if 'price' in item:
        return 13
    if 'gender' in item:
        return 14
    if 'product_description' in item:
        return 15
    
    # No Elements
    if len(item) == 0:
        return 16
    

def recomender(item:dict):
    if case_checker(item) == 1:
        logging.info('Case 1')
        return case_1(item)
    if case_checker(item) == 2:
        logging.info('Case 2')
        return case_2(item)
    if case_checker(item) == 3:
        logging.info('Case 3')
        return case_3(item)
    if case_checker(item) == 4:
        logging.info('Case 4')
        return case_4(item)
    if case_checker(item) == 5:
        logging.info('Case 5')
        return case_5(item)
    if case_checker(item) == 6:
        logging.info('Case 6')
        return case_6(item)
    if case_checker(item) == 7:
        logging.info('Case 7')
        return case_7(item)
    if case_checker(item) == 8:
        logging.info('Case 8')
        return case_8(item)
    if case_checker(item) == 9:
        logging.info('Case 9')
        return case_9(item)
    if case_checker(item) == 10:
        logging.info('Case 10')
        return case_10(item)
    if case_checker(item) == 11:
        logging.info('Case 11')
        return case_11(item)
    if case_checker(item) == 12:
        logging.info('Case 12')
        return case_12(item)
    if case_checker(item) == 13:
        logging.info('Case 13')
        return case_13(item)
    if case_checker(item) == 14:
        logging.info('Case 14')
        return case_14(item)
    if case_checker(item) == 15:
        logging.info('Case 15')
        return case_15(item)
    # No Elements
    if case_checker(item) == 16:
        logging.info('Case 16')



