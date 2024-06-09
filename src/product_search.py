import pandas as pd
import numpy as np
import os,json, sys
from langchain_voyageai import VoyageAIEmbeddings
from langchain_community.vectorstores import FAISS

groq_key = os.environ.get("GROQ_KEY")
voyage_api_key = os.environ.get("VOYAGE_KEY")

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


def similarity_search(quection:str, column:str):
    embedd_model = VoyageAIEmbeddings(voyage_api_key=voyage_api_key, model="voyage-2")

    # Get the absolute path to the file
    store = os.path.join(os.path.dirname(__file__), '..', 'artifacts', f'vcstore_{column}')
    new_db = FAISS.load_local(store, embedd_model,allow_dangerous_deserialization=True)

    embedd_query = embedd_model.embed_query(quection)
    result = new_db.similarity_search_with_score_by_vector(embedding=embedd_query, k=5, fetch_k=5)

    # Print to terminal
    for doc, score in result:
        print(f"Document ID: {doc.metadata['id']}, Page Content: {doc.page_content}, Score: {score}")
    # Save to text file
    path = os.path.join(os.path.dirname(__file__), '..', 'artifacts', f'results_{column}.txt')
    with open(path, 'w') as f:
        for doc, score in result:
            f.write(f"Document ID: {doc.metadata['id']}, Page Content: {doc.page_content}, Score: {score}\n")
    return result

similarity_search('lip balms','category')