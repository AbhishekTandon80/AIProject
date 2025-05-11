
import os
import pymongo
import pandas as pd
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from mistralai import Mistral
from openai import OpenAI

load_dotenv()
database_name = "storage"

collection_name = "df_storage"
collection_embedding = "embedding_storage"
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/?directConnection=true")
mistral_llm_client = Mistral(os.environ["MISTRAL_API_KEY"])
openai_llm_client = OpenAI()

def data_prep(file):
    # Process the uploaded file
    loader = PyPDFLoader(file_path= file, extract_images=True)
    pages = loader.load_and_split()

    # Split data
    # separators = ["\n\n", "\n", "(?<=\. )", " ", ""],
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""],
        length_function=len,
    )
    docs = text_splitter.split_documents(pages)

    # Calculate embeddings and store into MongoDB
    text_chunks = [text.page_content for text in docs]
    df = pd.DataFrame({'text_chunks': text_chunks})
    df_dict = df.to_dict(orient='records')
    database = get_database(database_name)
    get_collection(database, collection_name).insert_many(df_dict)

    return "PDF processed and data stored in MongoDB."



def get_embedding(df):
    df['embedding'] = df.text_chunks.apply(lambda x: get_embedding_from_mistral(x, mistral_llm_client))
    collection = get_collection()
    df_dict = df.to_dict(orient='records')
    collection.insert_many(df_dict)

    return "PDF processed and data stored in MongoDB."


def get_database(database_name):
    return mongoClient[database_name]

def get_collection(database, collection_name):
    # db.ListCollectionNames().ToList().Contains("cap2")
    collection = database[collection_name]
    return collection

def get_embedding_from_mistral(df, client):
    # text = text.replace("\n", " ")
    embeddings_batch_response = client.embeddings.create(
        model="mistral-embed",
        inputs=df["text_chunks"],
    )
    # print(embeddings_batch_response.data)
    return embeddings_batch_response.data

database = get_database(database_name)

if __name__ == "__main__":
    data_prep("../../data/PublicWaterMassMailing.pdf")