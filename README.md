# Biblioteca App 📚

Biblioteca App es un sistema de gestión de bibliotecas para registrar y controlar préstamos de libros, catálogo de ejemplares y base de usuarios. Este proyecto ha sido integrado para manejar cargas iniciales mediante archivos Excel y está listo para ser desplegado como una aplicación de tipo Monorepo en la nube de Vercel.

## 🛠️ Tecnologías usadas

### Frontend
- **React.js** (basado en componentes)
- **Vite** (bundler ultrarrápido)
- HTML, CSS y JS estándar

### Backend
- **Python 3**
- **FastAPI** (Framework web backend)
- **Pandas y Openpyxl** (Para lectura de base de datos inicial desde archivo Excel)

---

## 📋 Requisitos previos

Para poder ejecutar o modificar este proyecto localmente requieres tener:
1. **Node.js** (versión 18+ recomendada) y **npm**.
2. **Python** (versión 3.9+ recomendada).
3. Una cuenta de [Vercel](https://vercel.com) (solo para despliegue productivo).

---

## 🚀 Instalación y ejecución en local

### 1. Clona el repositorio y ubica la base de datos
Asegúrate de que el archivo maestro de Excel esté ubicado en la raíz del proyecto y lleve por nombre `BD_libros.xlsx`.

### 2. Configura y levanta el Backend
Abre una terminal y colócate en la carpeta del backend. Instala las dependencias y corre el servidor interactivo de FastAPI.

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
*El backend quedará levantado en `http://127.0.0.1:8000` y leerá automáticamente el archivo Excel.*

### 3. Configura y levanta el Frontend
En otra terminal desde la raíz, ingresa a la carpeta de React:

```bash
cd frontend
npm install
npm run dev
```
*El frontend quedará levantado (usualmente en `http://localhost:5173`) y se comunicará con el backend.*

---

## ☁️ Cómo desplegar en Vercel paso a paso

El proyecto está configurado para Vercel como un Monorepo integrando ambos servicios de forma transparente nativa.

1. **Sube tu código a GitHub** (incluye los archivos `.json`, el `BD_libros.xlsx`, las carpetas de `backend` y `frontend`).
2. Ingresa a Vercel con tu cuenta y presiona **Add New Project**.
3. Importa el repositorio que acabas de subir desde GitHub.
4. En la configuración de despliegue general (`Configure Project`), asegúrate de revisar:
   - **Framework Preset**: Selecciona *Vite* (o deja auto detectado si es capaz).
   - **Root Directory**: Déjalo en `./` (la carpeta raíz). El `vercel.json` autoconfigurará las rutas.
   - **Build Command**: Asegúrate de que detecta el comando en `package.json` de la raíz: `npm run build`.
5. Presiona **Deploy**. Vercel configurará dos pipelines automáticos: uno que toma React y lo buildea a un sitio estático, y otro que detecta tu `main.py` encapsulándolo como serverless function (gracias al archivo `vercel.json`).

Tu app será publicada en el dominio autogenerado por Vercel (e.g., `https://biblioteca-app.vercel.app`), funcionando con su Excel embebido en memoria.

---

## 🔐 Variables de entorno necesarias

Actualmente, el proyecto funciona directamente de forma estática y en memoria por lo que **no se necesitan variables de entorno** para su uso primario. 
*Nota futura:* Si el frontend requiere apuntar estáticamente a otro backend remoto, puede habilitarse una variable de Vite local en `.env`. Vercel rutea los endpoints en `/api/*` directamente a tu backend relativo de forma oculta en producción.

---

