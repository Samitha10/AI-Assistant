import os,sys
# Add the project root to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from product_search import similarity_search
from utils.logger import logging
from utils.exception import CustomException
from product_search import id_extractor,price_filter
from data_processor import data_file_importer

def case_1(item:dict):
    category = item['product_category'] + ' ' + item['gender']
    price = item['price']
    description = item['product_description']

    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category',10,20)
    output1 = {}
    for doc, score in items1:
        id = doc.metadata['id']
        output1[id] = score
    
    # Perform similarity search based on the description
    items2 = similarity_search(description, 'description', 10, 20)
    output2 = {}
    for doc, score in items2:
        id = doc.metadata['id']
        output2[id] = score
    ids = id_extractor(output1, output2,5)
    price_staus = price_filter(ids,price,5)

    return ids,price_staus

#                                           Three-element subsets
def case_2(item:dict):
    category = item['product_category'] + ' ' + item['gender']
    price = item['price']
    
    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category',5,20)
    ids = []
    for doc, score in items1:
        ids.append({doc.metadata['id']})
    
    price_staus = price_filter(ids, price, 5)
    
    return ids,price_staus

def case_3(item:dict):
    category = item['product_category']
    price = item['price']
    description = item['product_description']

    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category', 5, 20)
    output1 = {}
    for doc, score in items1:
        id = doc.metadata['id']
        output1[id] = score

    # Perform similarity search based on the description
    items2 = similarity_search(description, 'description', 5, 20)
    output2 = {}
    for doc, score in items2:
        id = doc.metadata['id']
        output2[id] = score
    ids = id_extractor(output1, output2, 5)
    price_staus = price_filter(ids, price, 5)

    return ids,price_staus

def case_4(item:dict):
    category = item['product_category'] + ' ' + item['gender']
    description = item['product_description']

    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category',10,20)
    output1 = {}
    for doc, score in items1:
        id = doc.metadata['id']
        output1[id] = score
    
    # Perform similarity search based on the description
    items2 = similarity_search(description, 'description', 10, 20)
    output2 = {}
    for doc, score in items2:
        id = doc.metadata['id']
        output2[id] = score
    ids = id_extractor(output1, output2,5)
    

    return ids

def case_5(items:dict):
    price = items['price']
    category = items['gender']
    description = items['product_description']

    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category',10,20)
    output1 = {}
    for doc, score in items1:
        id = doc.metadata['id']
        output1[id] = score
    
    # Perform similarity search based on the description
    items2 = similarity_search(description, 'description', 10, 20)
    output2 = {}
    for doc, score in items2:
        id = doc.metadata['id']
        output2[id] = score
    ids = id_extractor(output1, output2,5)
    price_staus = price_filter(ids,price,5)

    return ids,price_staus

#                                           Two element subsets

# category, price
def case_6(item:dict):
    category = item['product_category']
    price = item['price']

    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category',5,10)
    ids = []
    for doc, score in items1:
        ids.append({doc.metadata['id']})

    price_staus = price_filter(ids, price, 5)
    return ids,price_staus

# category, gender
def case_7(item:dict):
    category = item['product_category'] + ' ' + item['gender']

    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category', 5, 10)
    ids = []
    for doc, score in items1:
        ids.append({doc.metadata['id']})
    return ids

# category, description
def case_8(item:dict):
    category = item['product_category']
    description = item['product_description']

    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category', 5, 20)
    output1 = {}
    for doc, score in items1:
        id = doc.metadata['id']
        output1[id] = score

    # Perform similarity search based on the description
    items2 = similarity_search(description, 'description', 5, 20)
    output2 = {}
    for doc, score in items2:
        id = doc.metadata['id']
        output2[id] = score
    ids = id_extractor(output1, output2, 5)
    return ids

# price, gender
def case_9(item:dict):
    price = item['price']
    category = item['gender']

    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category', 5, 10)
    ids = []
    for doc, score in items1:
        ids.append({doc.metadata['id']})

    price_staus = price_filter(ids, price, 5)
    return ids,price_staus

# price, description
def case_10(item:dict):
    price = item['price']
    description = item['product_description']

    # Perform similarity search based on the description
    items = similarity_search(description, 'description', 5, 20)
    ids = []
    for doc, score in items:
        ids.append({doc.metadata['id']})

    price_staus = price_filter(ids, price, 5)
    return ids,price_staus


#gender, description
def case_11(item:dict):
    category = item['gender']
    description = item['product_description']

    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category', 5, 20)
    output1 = {}
    for doc, score in items1:
        id = doc.metadata['id']
        output1[id] = score

    # Perform similarity search based on the description
    items2 = similarity_search(description,'description', 5, 20)
    output2 = {}
    for doc, score in items2:
        id = doc.metadata['id']
        output2[id] = score
    ids = id_extractor(output1, output2, 5)
    return ids

#                                            One element subsets

# category
def case_12(item:dict):
    category = item['product_category']

    # Perform similarity search based on the category
    items = similarity_search(category, 'category', 5, 10)
    ids = []
    for doc, score in items:
        ids.append({doc.metadata['id']})
    return ids

# price
def case_13(item:dict):
    price = item['price']
    range = 5
    df = data_file_importer()

    filtered_df = df[df['price'].between(price - range, price + range)]
    ids = filtered_df['id'][:10].tolist()
    return ids

# gender
def case_14(item:dict):
    category = item['gender']

    # Perform similarity search based on the category
    items = similarity_search(category, 'category', 5, 10)
    ids = []
    for doc, score in items:
        ids.append({doc.metadata['id']})
    return ids

# description
def case_15(item:dict):
    description = item['product_description']
    # Perform similarity search based on the description
    items = similarity_search(description, 'description', 5, 20)
    ids = []
    for doc, score in items:
        ids.append({doc.metadata['id']})
    return ids


#                                            No elements
def case_16():
    df = data_file_importer()
    random_ids = df['id'].sample(n=5, random_state=42).tolist()
    return random_ids





















item = {
    'product_category': 'lip balms',
    'gender': 'Men',
    'price': 20,
    'product_description': 'Avocado & Wheatgerm oils'
}

case_1(item)







