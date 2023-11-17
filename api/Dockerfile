FROM python:3.9

ENV        REDIS_URL="redis://localhost:6379"
WORKDIR /app

# Actualiza el índice del paquete y instala las dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    libfreetype6-dev \
    libgfortran5 && \
    rm -rf /var/lib/apt/lists/*

# Copia los archivos de la aplicación
COPY . /app

# Instala las dependencias necesarias
RUN pip install -r requirements.txt

# CMD para ejecutar tu aplicación
CMD ["python", "./app.py"]
