# %%
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import os

app = FastAPI()
# %%
# Configuração do Modelo de PLN (Sentence Transformers)
# O ChromaDB usará este modelo para a geometria dos vetores
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2" # Modelo padrão, leve e eficiente
)

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(
    name="rag_geometrico",
    embedding_function=sentence_transformer_ef,
    metadata={"hnsw:space": "cosine"}
)

class Item(BaseModel):
    texto: str

@app.post("/transpor")
async def transpor(item: Item):
    # Manobra de busca na variedade estatística
    res = collection.query(query_texts=[item.texto], n_results=1)
    contexto = res['documents'][0][0] if res['documents'][0] else "Sem dados."
    return {"resposta": f"Processamento PLN: {contexto}"}

@app.post("/alimentar")
async def alimentar(item: Item):
    import uuid
    collection.add(documents=[item.texto], ids=[str(uuid.uuid4())])
    return {"status": "Informação parametrizada"}
# %%
