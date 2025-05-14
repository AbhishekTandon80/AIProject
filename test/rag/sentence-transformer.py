# docker pull pgvector/pgvector:pg16
# docker run --name postgres -p 5432:5432 POSTGRES_USER=myuser -e POSTGRES_PASSWORD=password -d pgvector/pgvector:pg16
from  psycopg2  import connect
from pgvector.psycopg2 import register_vector
import numpy as np

from sentence_transformers import SentenceTransformer

conn_string = "host='localhost' dbname='myuser' user='myuser' password='password'"
conn = connect(conn_string)
conn.autocommit = True
cur = conn.cursor()

cur.execute('CREATE EXTENSION IF NOT EXISTS vector')
register_vector(conn)

cur.execute('DROP TABLE IF EXISTS documents')
cur.execute('CREATE TABLE documents (id bigserial PRIMARY KEY, content text, embedding vector(384))')

model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

input = [
    'The dog is barking',
    'The cat is purring',
    'The bear is growling'
]
embeddings = model.encode(input)
for content, embedding in zip(input, embeddings):
    cur.execute('INSERT INTO documents (content, embedding) VALUES (%s, %s)', (content, embedding))

# conn.commit()
query = 'who is barking?'
query_embedding = model.encode(query)

command = "SELECT id, content FROM documents ORDER BY embedding <=> \'" + str(query_embedding.tolist()) + "\' LIMIT 1;"
print(command)
cur.execute(command)
results = cur.fetchall()
print(results)

print("Execution completed")