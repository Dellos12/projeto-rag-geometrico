# %%
import json
import uuid

# %%
class MCPHandler:
    def __init__(self, motor_rag):
        self.motor = motor_rag
# %%
def formatar_requisição_mcp(self, pergunta):
    """
    Simular a Torre A parametrizando a pergunta para a Geodésica
    """
    return {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "retrievel_geometric_context",
            "arguments": {"query": pergunta}
        },
        "id": str(uuid.uuid4())
    }
# %%
def processar_resposta_mcp(self, json_rpc_request):
    metodo = json_rpc_request.get("method")
    params = json_rpc_request.get("params", {})
    query = params.get("arguments", {}).get("query")

    if metodo == "tools/call":
        # 1. (Busca geométrica)
        resultado_bruto = self.motor.consultar(query)

        # 2. Empacotamento JSON-RPC
        return {
            "jsonrpc": "2.0",
            "result": {
                "content": f"Contexto Geodésico local: {resultado_bruto}",
                "metadata": {
                    "norma": "cosine",
                    "status": "parametrizado"
                }
            },
            "id": json_rpc_request.get("id")
        }
# %%
