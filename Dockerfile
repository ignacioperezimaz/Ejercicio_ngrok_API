
# Utilizamos Python 3.12
FROM python:3.12-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos las dependencias
COPY requirements.txt .

# Instalamos las librerías
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de nuestra API
COPY . .

# Puerto de nuestra aplicación
EXPOSE 8000

# Arrancamos FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
