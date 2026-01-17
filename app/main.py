# %%
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import os
import uuid
from typing import Union
from sentence_transformers import CrossEncoder

app = FastAPI(title="Motor RAG Geométrico - MCP Ready")
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

reranker_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

class Item(BaseModel):
    texto: str


class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict
    id: Union[str, int]

#@app.post("/transpor")
#async def transpor(item: Item):
    # Manobra de busca na variedade estatística
#    res = collection.query(query_texts=[item.texto], n_results=1)
#    contexto = res['documents'][0][0] if res['documents'][0] else "Sem dados."
#    return {"resposta": f"Processamento PLN: {contexto}"}

@app.post("/alimentar")
async def alimentar(item: Item):
    id_unico = str(uuid.uuid4())
    collection.add(documents=[item.texto], ids=[id_unico])
    return {"status": "Informação parametrizada", "id": id_unico} 

# %%
@app.post("/mcp/v1")
async def mcp_v1(rpc: JsonRpcRequest):
    """
    Endpoint MCP: via JSON-RPC 2.0
    """
    if rpc.method == "tools/call":
        query = rpc.params.get("arguments", {}).get("query")
        if not query:
            raise HTTPException(status_code=400, details="Query ausente")
        
        # Manobra na Varidade Estatística
        res = collection.query(query_texts=[query], n_results=3)
        
        # Fallback se o Data Lake estiver vazio
        if not res['documents'] or not res['documents'][0]:
            return {
                "jsonrpc": "2.0",
                "id": rpc.id,
                "result": {"content": "Vacuo informativo: Sem dados na coleção."}

            }

        candidato = res['documents'][0]
        distancias_geo = res['distances'][0]

        # o Cross-encoder calcula a relevância entre a pergunta e cada Resposta
        pares = [[query, doc]for doc in candidato]
        scores_refino = reranker_model.predict(pares)

        melhor_idx = scores_refino.argmax()
        vencedor = candidato[melhor_idx]
        confianca_refino = float(scores_refino[melhor_idx])

        return {
            "jsonrpc": "2.0",
            "id": rpc.id,
            "result": {
                "content": vencedor,
                "metadata": {
                    "distancia_geometria_inicial":float(distancias_geo[melhor_idx]),
                    "score_refino_confianca":confianca_refino,
                    "engine": "Hybrid-two-Tower-RAG",
                    "norm": "cosine"
                }
            }
        }
    
    return {
        "jsonrpc": "2.0",
        "id": rpc.id,
        "error": {
            "code": -32601,
            "message": "Método não encontrado"
        }
    }

# %%
