import pandas as pd
import numpy as np
from langchain_voyageai import VoyageAIEmbeddings
from langchain_community.vectorstores import FAISS

import os,json


# # Extract necessary columns
# df = pd.read_csv("data.csv")

# # Create a new DataFrame with selected columns
# df = df[['id', 'category', 'categorie']]

# # Convert the DataFrame to a JSON string
# json_string = df.to_json(orient='records')

# # Write the JSON string to a file
# with open('output.json', 'w') as f:
#     f.write(json_string)


groq_key = os.environ.get("GROQ_KEY")
voyage_api_key = os.environ.get("VOYAGE_KEY")
print(voyage_api_key)

embedd_model = VoyageAIEmbeddings(voyage_api_key=voyage_api_key, model="voyage-2")

# Load the JSON data from the file into a variable
with open('output.json', 'r') as f:
    data = json.load(f)


# Extract categories and ids
categories = [item["category"] for item in data]
ids = [item["id"] for item in data]

embeddings = embedd_model.embed_documents(categories)
vcstore = FAISS.add_embeddings(
    text_embeddings=embeddings,
    ids=ids,
)