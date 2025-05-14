from time import sleep

from dotenv import load_dotenv

from create_text_from_pdf import get_collection
from create_text_from_pdf import database
from create_text_from_pdf import collection_embedding_df
from create_text_from_pdf import mistral_llm_client
from create_text_from_pdf import openai_llm_client

load_dotenv()

llm_client = "mistral"
model = None
client = None

if llm_client == "mistral":
    model = "mistral-embed"
    client = mistral_llm_client
else:
    model = "text-embedding-ada-002"
    client = openai_llm_client


def find_similar_documents(embedding):
    collection = get_collection(database, collection_embedding_df)
    documents = list(
        collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "default",
                    "path": "'embedding'",
                    "queryVector": embedding,
                    "numCandidates": 20,
                    "limit": 10,
                    "similarity": "cosine"
                }
            },
            {"$project": {"_id": 0, "text_chunks": 1}}
        ]))
    return documents

def qna(users_question):

    embeddings_batch_response = client.embeddings.create(
        model=model,
        inputs=users_question,
    )
    # print(embeddings_batch_response.data)
    question_embedding = embeddings_batch_response.data[0].embedding
    sleep(2)

    # question_embedding = get_embedding_from_mistral(users_question, client)
    print("-----Here is user question------")
    print(users_question)
    documents = find_similar_documents(question_embedding)

    print("-----Retrieved documents------")
    print(documents)
    for doc in documents:
        doc['text_chunks'] = doc['text_chunks'].replace('\n', ' ')

    for document in documents:
        print(str(document) + "\n")

    context = " ".join([doc["text_chunks"] for doc in documents])
    template = f"""
    You are an expert who loves to help people! Given the following context sections, answer the
    question using only the given context. If you are unsure and the answer is not
    explicitly written in the documentation, say "Sorry, I don't know how to help with that."

    Context sections:
    {context}

    Question:
    {users_question}

    Answer:
    """
    messages = [{"role": "user", "content" : template}]

    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=messages,
    )
    formatted_documents = '\n'.join([doc['text_chunks'] for doc in documents])

    return chat_response.choices[0].message, formatted_documents



if __name__ == "__main__":
    qna('laboratory.TheOpenELIS(OE)LIMSwillprovidethelaboratorywithimprovedsamplemanagement')
