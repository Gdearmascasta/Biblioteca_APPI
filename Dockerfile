# Etapa 1: Build del frontend
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend

# Copiar archivos de dependencias e instalarlas
COPY frontend/package*.json ./
RUN npm install

# Copiar el codigo fuente del frontend y compilar (Vite)
COPY frontend/ ./
RUN npm run build

# Etapa 2: Backend y servir la aplicación completa
FROM python:3.10-slim
WORKDIR /app

# Instalar dependencias del backend
COPY api/requirements.txt ./api/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r api/requirements.txt

# Copiar código del backend y base de datos (BD_libros.xlsx)
COPY api/ ./api/

# Copiar el build del frontend construido en la etapa 1
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Agregar api al PYTHONPATH para que los imports locales funcionen
ENV PYTHONPATH=/app/api

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la aplicación (Uvicorn), Railway utiliza la variable PORT
CMD sh -c "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"
