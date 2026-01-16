# %%

import requests
import questionary
from rich.console import Console
from rich.panel import Panel

import nest_asyncio
nest_asyncio.apply()

console = Console()
# %%
# %%
def loop():
    url = "http://localhost:8000/transpor"
    
    while True:
        # 1. Captura a pergunta
        p = questionary.text("Pergunta para o RAG:").ask()
        
        # 2. Verifica se o usuário quer sair
        if not p or p.lower() == 'sair':
            break
        
        try:
            # 3. Define 'r' enviando a requisição para o FastAPI
            response = requests.post(url, json={"texto": p})
            response.raise_for_status() # Garante que a requisição funcionou
            
            # 4. Extrai o JSON
            dados = response.json()
            
            # 5. Busca a chave correta (tentando as duas variações que usamos)
            texto_final = dados.get('resposta', dados.get('resposta_natural', 'Chave não encontrada no JSON'))
            
            # 6. Manobra a saída no terminal com Rich
            console.print(Panel(texto_final, title="Saída Transposta", border_style="blue"))
            
        except Exception as e:
            console.print(f"[bold red]Erro na comunicação:[/bold red] {e}")

if __name__ == "__main__":
    loop()
# %%
