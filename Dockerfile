
FROM python:3.10-slim

WORKDIR /app

# Instala dependências de sistema apenas uma vez
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Camada de Cache Pesada: Só rodará de novo se o .requirements.lock mudar
COPY requirements.txt .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Camada Leve: Onde seu código entra (muda toda hora, mas o build será instantâneo)
COPY . .

# ... (restante do arquivo igual)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
