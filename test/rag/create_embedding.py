from create_text_from_pdf import get_database
from create_text_from_pdf import get_collection
import pandas as pd
import tiktoken
from create_text_from_pdf import openai_llm_client
from create_text_from_pdf import mistral_llm_client
from create_text_from_pdf import database_name
from create_text_from_pdf import collection_raw_df
from create_text_from_pdf import get_embedding_from_mistral
from create_text_from_pdf import collection_embedding_df
from create_text_from_pdf import database
from time import sleep

def load_and_process_from_db(limit: int):
    database = get_database(database_name)
    data = list(get_collection(database, collection_raw_df).find().limit(limit))
    # print("Data retrieved from MongoDB:", data)
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

# Utility to count token based on openai model
def num_tokens_from_df(df: pd.DataFrame) -> int:
    # df = load_and_process_from_db()
    count = 0
    encoding = tiktoken.encoding_for_model("text-embedding-ada-002")
    for text in df["text_chunks"]:
        token_integers = encoding.encode(text)
        token_length = len(token_integers)
        count += token_length
        # print("length:", token_length)
        # token_bytes = [encoding.decode_single_token_bytes(token) for token in token_integers]
        # print(f"token bytes: {token_bytes}")
    print("Total token count:", count)
    return count

# def get_embedding_from_openai(df: pd.DataFrame):

llm_client = "mistral"
model = None
client = None

if llm_client == "mistral":
    model = "mistral-embed"
    client = mistral_llm_client
else:
    model = "text-embedding-ada-002"
    client = openai_llm_client

row_count: int = 1000_000
size = 100

def add_embedding(index, data):
    value = data[index % size].embedding
    return value


# Generate embedding for text using mistral embedding model
if __name__ == "__main__":
    df = load_and_process_from_db(row_count)
    length = len(df)
    count = (len(df)) // size + 1
    for x in range(count):
        start = x * size
        end = min((x + 1) * size, len(df))
        df_subset = df[start:end]
        sleep(2)
        embedding_data = get_embedding_from_mistral(df_subset, client)
        df_subset["embedding"] = df_subset.apply(lambda row: add_embedding(row.name, embedding_data), axis = 1)
        df_subset = df_subset.drop('_id', axis=1)
        get_collection(database, collection_embedding_df).insert_many(df_subset.to_dict(orient='records'))
        print("Insert completed into database for batch...")




