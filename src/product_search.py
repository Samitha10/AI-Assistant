import json
import os,sys
# Add the project root to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from langchain_voyageai import VoyageAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.data_processor import data_file_importer
from functools import lru_cache



# Creating JSON files from CSV
def jsonize_data():
    # Extract necessary columns
    df = pd.read_csv("DataFiles/data.csv")

    # Create a new DataFrame with selected columns
    df = df[['id', 'category', 'description']]

    # Convert the DataFrame to a JSON string
    json_string = df.to_json(orient='records')

    # Write the JSON string to a file
    with open('DataFiles/dataRecords.json', 'w') as f:
        f.write(json_string)
    print("JSON file created successfully!")

# Save vector store
def save_vector_store(column:str):
    voyage_api_key = os.environ.get("VOYAGE_KEY")
    embedd_model = VoyageAIEmbeddings(voyage_api_key=voyage_api_key, model="voyage-2")

    # Load the JSON data from the file into a variable
    with open('DataFiles/dataRecords.json', 'r') as f:
        data = json.load(f)

    # Extract categories and ids
    categories = [item[column] for item in data]
    ids = [item["id"] for item in data]
    metadata = [{"id": id} for id in ids]

    vcstore = FAISS.from_texts(categories,embedd_model,metadatas=metadata)
    vcstore.save_local(f'artifacts/vcstore_{column}')

@lru_cache(maxsize=128, typed=False)
def model_loader():
    voyage_api_key = os.environ.get("VOYAGE_KEY")
    embedd_model = VoyageAIEmbeddings(voyage_api_key=voyage_api_key, model="voyage-2")
    return embedd_model

@lru_cache(maxsize=128, typed=False)
def embedd_loader(column:str):
    store = os.path.join(os.path.dirname(__file__), '..', 'artifacts', f'vcstore_{column}')
    data = FAISS.load_local(store, model_loader(),allow_dangerous_deserialization=True)
    return data

@lru_cache(maxsize=128, typed=False)
def similarity_search(quection:str, column:str,k:int,fetch_k:int):
    # Load the vector store
    DATA = embedd_loader(column)    
    embedd_query = model_loader().embed_query(quection)
    result = DATA.similarity_search_with_score_by_vector(embedding=embedd_query,k=k,fetch_k=fetch_k)

    # # Print to terminal
    # for doc, score in result:
    #     print(f"Document ID: {doc.metadata['id']}, Page Content: {doc.page_content}, Score: {score}")
    # # Save to text file
    # path = os.path.join(os.path.dirname(__file__), '..', 'artifacts', f'results_{column}.txt')
    # with open(path, 'w') as f:
    #     for doc, score in result:
    #         f.write(f"Document ID: {doc.metadata['id']}, Page Content: {doc.page_content}, Score: {score}\n")
    return result


def id_extractor(dict1:dict, dict2:dict,count:int):
    # Identify common keys
    common_keys = set(dict1.keys()).intersection(dict2.keys())
    common_keys = list(common_keys)
    # If there are more common keys than needed, truncate the list
    if len(common_keys) > 5:
        common_keys = common_keys[:5]

    # If the number of common keys is less than 5, add keys with the lowest values from both dictionaries
    if len(common_keys) < 5:
        # Get items sorted by value from both dictionaries
        sorted_dict1_items = sorted(dict1.items(), key=lambda item: item[1])
        sorted_dict2_items = sorted(dict2.items(), key=lambda item: item[1])
        
        # Create a list of all items, excluding the common keys
        combined_items = sorted_dict1_items + sorted_dict2_items
        combined_items = [(k, v) for k, v in combined_items if k not in common_keys]
        
        # Add keys with the lowest values until we have 5 keys in total
        for k, v in combined_items:
            if len(common_keys) >= 5:
                break
            common_keys.append(k)

    # Ensure we have exactly 5 keys
    keys = common_keys[:5]
    return keys


def price_filter(ids: list, price, range: int):
    df = data_file_importer()
    results = []

    # Check if price is a numeric value (float or int)
    if not isinstance(price, (float, int)):
        return [True] * len(ids)

    for id in ids:
        if id in df['id'].values:
            id_price = df.loc[df['id'] == id, 'price'].values[0]
            if abs(id_price - price) <= range:
                results.append(True)
            else:
                results.append(False)
        else:
            results.append(False)  # Assuming IDs not found should be marked False

    return results

def price_extractor(ids: list):
    df = data_file_importer()
    results = []

    for id in ids:
        if id in df['id'].values:
            id_price = df.loc[df['id'] == id, 'price'].values[0]
            results.append(id_price)
    return results

