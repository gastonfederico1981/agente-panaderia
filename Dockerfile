FROM python:3.11-slim

WORKDIR /app

# Copiamos los archivos de requerimientos
COPY requirements.txt .

# Instalamos solo lo necesario de Python (evitamos apt-get que está fallando)
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Usamos el puerto de Render
EXPOSE 10000

CMD ["sh", "-c", "streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0"]