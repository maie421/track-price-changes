import numpy as np
import pandas as pd
from openai import OpenAI

datafile_path = "file/product_test_embedding.csv"

df = pd.read_csv(datafile_path)

client = OpenAI(
    api_key="",
)


def cosine_similarity(a, b):
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    return np.dot(a, b) / (np.linalg.norm(a) * (np.linalg.norm(b)))


def convert_to_array(embedding_string):
    return np.fromstring(embedding_string[1:-1], sep=',')


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def search_products(df, product_description, n=3):
    df = df.dropna(subset=['ada_embedding'])
    df['ada_embedding'] = df['ada_embedding'].apply(convert_to_array)

    embedding = get_embedding(product_description, model='text-embedding-ada-002')
    df['similarities'] = df.ada_embedding.apply(lambda x: cosine_similarity(x, embedding))
    res = df.sort_values('similarities', ascending=False).head(n)
    return res


