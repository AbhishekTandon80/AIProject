from  psycopg2  import connect
from pgvector.psycopg2 import register_vector
import numpy as np
# from pgvector.psycopg import register_vector


# Connect to the database
conn_string = "host='localhost' dbname='myuser' user='myuser' password='password'"
conn = connect(conn_string)
conn.autocommit = True
cur = conn.cursor()
register_vector(conn)

# --- Drop a pgvector table ---
cur.execute('DROP TABLE IF EXISTS vectors')

# --- Create a pgvector table ---
create_table_command = """
CREATE TABLE vectors (
    id bigserial PRIMARY KEY,
    embedding vector(3)
);
"""
cur.execute(create_table_command)
conn.commit()
cur.close()

# --- Insert a vector ---
cur = conn.cursor()
vector_data = [1.0, 2.0, 3.0]  # Example vector
cur.execute("INSERT INTO vectors (embedding) VALUES (%s);", (vector_data,))
vector_data2 = [1.0, -2.0, 4.0]  # Example vector
cur.execute("INSERT INTO vectors (embedding) VALUES (%s);", (vector_data2,))
conn.commit()
cur.close()

# --- Perform a similarity search ---
cur = conn.cursor()
query_vector = [1.0, 2.0, 3.0]  # Your query vector
command = "SELECT id, embedding FROM vectors ORDER BY embedding <=> \'" + str(query_vector) + "\' LIMIT 1;"
print(command)
cur.execute(command)
results = cur.fetchall()
print(results)  # Print the IDs of the most similar vectors
cur.close()

# --- Close the database connection ---
conn.close()