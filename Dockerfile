# Usamos una imagen liviana de Python
FROM python:3.11-slim

# Evitamos que Python genere archivos .pyc y que el output se guarde en cache
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Seteamos la carpeta de trabajo dentro del servidor
WORKDIR /app

# Instalamos dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el requirements y lo instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto que usa Streamlit (8501)
EXPOSE 8501

# Comando para arrancar la app
ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]