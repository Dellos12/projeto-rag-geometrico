# 🌀 Geometric RAG Engine: High-Abstraction Information Retrieval

Este repositório apresenta uma implementação avançada de **Retrieval-Augmented Generation (RAG)** focada na **Geometria da Informação**. O projeto transpõe dados de negócios para variedades estatísticas, permitindo que a inteligência artificial navegue por contextos através de relações métricas e espaciais.

## 🧠 Fundamentação Matemática e Estatística

Diferente de implementações triviais, este motor explora a **Geometria dos Tensores** e a **Análise de Variedades**:
*   **Representação Vetorial:** Conversão de strings em vetores de 384 dimensões (`all-MiniLM-L6-v2`), criando um espaço métrico onde a semântica é quantificada.
*   **Regulação de Normas:** Utilização da **Métrica de Cosseno** para calcular a proximidade angular entre vetores, garantindo que o "diálogo" entre a pergunta e o dado seja filtrado por relevância estatística.
*   **Interoperabilidade via MCP:** Integração do **Model Context Protocol (MCP)** para padronizar o diálogo entre a infraestrutura local e modelos globais via **JSON-RPC**.

## 🏗️ Arquitetura do Ecossistema

O projeto foi desenhado como uma "engrenagem" capaz de se acoplar a estruturas maiores (Data Lakes, Azure, Clusters):

*   **Docker & Docker Compose:** Orquestração de camadas isoladas para garantir a consistência do ambiente de cálculo.
*   **FastAPI:** Interface assíncrona para transposição de dados em tempo real.
*   **ChromaDB:** Banco vetorial persistente utilizando indexação **HNSW** (Hierarchical Navigable Small Worlds).
*   **NumPy:** Motor fundamental para manipulação de arrays multidimensionais e cálculo de normas.

## 🚀 Como Executar a Manobra

### 1. Subir a Infraestrutura (Docker)
```bash
docker compose up --build -d
