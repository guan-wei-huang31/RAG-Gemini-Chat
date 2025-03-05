##############################################################################
#Filename: rag_api.py
#Author: Guan-Wei Huang
#Created: 2025-03-04
#Version: 1.0.0
#License: MIT
#Description: 
#    This script sets up a Flask API for retrieving product information using 
#    a combination of structured SQL queries and vector-based retrieval (RAG).
#    It integrates with SQLite and ChromaDB for efficient data retrieval.
#    
#Contact: gwhuang24@gmail.com
#GitHub: https://github.com/guan-wei-huang31
##############################################################################

from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import chromadb
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

# **1. Flask setup**
app = Flask(__name__)
CORS(app)

# **2.Setting Gemini API Key 
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

# **3. SQLite connection**
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "functional_products.db")
db_uri = f"sqlite:///{DB_PATH}"
engine = create_engine(db_uri)

# **4. Retrieve information from database**
query = """
    SELECT product_name, weight, manufacturer, expiration_date, storage_method, 
           delivery_time, reference_price, allergy_info, in_stock, 
           certifications, health_description, product_details 
    FROM Functional_Products
"""
df = pd.read_sql(query, engine)

# **5. Transfer to dataframe**
df["text"] = df.apply(lambda row: f"Product Name: {row['product_name']} is manufactured by {row['manufacturer']}.\n"
                                  f"It weighs {row['weight']}g and is priced at {row['reference_price']} USD.\n"
                                  f"The product is described as: {row['health_description']}.\n"
                                  f"Key details: {row['product_details']}.\n"
                                  f"Storage Method: {row['storage_method']}.\n"
                                  f"Stock Status: {'In Stock' if int(row['in_stock']) == 1 else 'Out of Stock'}.\n"
                                  f"Certifications: {row['certifications']}.\n"
                                  f"Allergy Information: {row['allergy_info']}.\n"
                                  f"Expiration Date: {row['expiration_date']}.\n"
                                  f"Delivery Time: {row['delivery_time']}.\n", axis=1)

# **6. Define embedding model**
def get_embedding(text):
    response = client.models.embed_content(
        model="models/text-embedding-004",
        contents=text,
    )
    return response.embeddings[0].values

# **7. Process vectorDB **
vector_db = chromadb.PersistentClient(path="./chroma_db")
collection = vector_db.get_or_create_collection(name="functional_products")


for _, row in df.iterrows():
    embedding_vector = get_embedding(row["text"])
    collection.add(
        ids=[str(row["product_name"])], 
        embeddings=[embedding_vector], 
        documents=[row["text"]]
    )

# **8. Retrieve from vectorDB **
def retrieve_from_vector_db(input_text):
    query_embedding = get_embedding(input_text)
    results = collection.query(query_embeddings=[query_embedding], n_results=3)

    if not results["documents"] or not results["documents"][0]:
        return "No relevant information found."

    return results["documents"][0][0] 

# **9. Prompt engineering setup**
def ask_gemini(context, input_text):
    prompt =  f"""
    You are an AI assistant answering product-related questions. 
    Use the following retrieved product information to generate a concise response.

    Below is the relevant product information retrieved from the database: "{context}"

    The user asked: "{input_text}"
    
    If the context contains the answer, reply concisely using the provided details.
    If the context does not have the answer, say: "I'm sorry, I don't have enough details."

    Always keep the response within 30 words.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt])
    return response.candidates[0].content.parts[0].text.strip()

# **10. Flask API**
@app.route("/ask", methods=["POST"])
def ask_question():

    data = request.json
    input_text = data.get("question", "").strip()
    
    if not input_text:
        return jsonify({"error": "No question provided"}), 400

    retrieval_results = retrieve_from_vector_db(input_text)
    context = retrieval_results if retrieval_results else []

    answer = ask_gemini(context, input_text)

    return jsonify({"answer": answer})

# **Start Flask API**
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)

