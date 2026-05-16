import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

VECTOR_STORE_NAME = os.getenv("VECTOR_STORE_NAME", "openai-rag-demo")

vector_store = client.vector_stores.create(name=VECTOR_STORE_NAME)

print("VECTOR_STORE_ID =", vector_store.id)
print("STATUS =", vector_store.status)
print("FILE_COUNTS =", vector_store.file_counts)