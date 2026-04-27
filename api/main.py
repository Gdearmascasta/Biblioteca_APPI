from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import datetime
import pandas as pd
import os
import sys

# Agregar el directorio actual al sys.path para que los imports locales funcionen correctamente en entornos como Railway
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from servicios.biblioteca import Biblioteca
from modelos.entidades import Libro, Autor, Editorial, Nacionalidad, Usuario

app = FastAPI(title="Biblioteca Digital API")

# Setup CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción especificar dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global de la biblioteca
biblio = Biblioteca()

# Cargar datos desde BD_libros.xlsx
# Utilizar una ruta absoluta o relativa basada en la ubicación del archivo en el despliegue Vercel o en local
base_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_dir, "BD_libros.xlsx")

try:
    df = pd.read_excel(excel_path)
    for index, row in df.iterrows():
        cod = int(row['CÓDIGO']) if pd.notna(row['CÓDIGO']) else 0
        tit = str(row['TÍTULO']) if pd.notna(row['TÍTULO']) else "Desconocido"
        edi = str(row['EDITORIAL']) if pd.notna(row['EDITORIAL']) else "Desconocida"
        autores_str = str(row['AUTOR(ES)']) if pd.notna(row['AUTOR(ES)']) else "Anónimo"

        edt_obj = Editorial(1, edi)
        lib_obj = Libro(cod, tit, edt_obj)
        
        # Separar autores si vienen separados por coma (asumiendo ese formato)
        autores_separados = [a.strip() for a in autores_str.split(',')]
        for a_nombre in autores_separados:
            nac = Nacionalidad(1, "Desconocida")
            aut_obj = Autor(1, a_nombre, "", "", nac)
            lib_obj.agregar_autor(aut_obj)
            
        biblio.registrar_libro(lib_obj)
    print(f"Cargados {len(df)} libros desde {excel_path}")
except Exception as e:
    print(f"Error cargando Excel: {e}")

usu = Usuario(1, "Carlos Gómez", "Calle 123", "3000000000")
biblio.registrar_usuario(usu)



# --- Schemas Pydantic ---
class LibroCreate(BaseModel):
    codigo: int
    titulo: str
    editorial_nombre: str
    autores_nombres: List[str]

class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    editorial_nombre: Optional[str] = None
    autores_nombres: Optional[List[str]] = None

class UsuarioCreate(BaseModel):
    codigo: int
    nombre: str
    direccion: str
    telefono: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None

class PrestamoCreate(BaseModel):
    codigo_usuario: int
    codigos_libros: List[int]
    fecha_pres: Optional[str] = None

class PrestamoUpdate(BaseModel):
    dias_en_mora: Optional[int] = None

# --- Endpoints Libros ---
@app.get("/api/libros")
def get_libros():
    libros = biblio.listar_libros()
    return {"libros": [l.to_dict() for l in libros]}

@app.post("/api/libros")
def crear_libro(req: LibroCreate):
    edt = Editorial(100, req.editorial_nombre)  # Simplificado para probar
    lib = Libro(req.codigo, req.titulo, edt)
    for n_aut in req.autores_nombres:
        a = Autor(100, n_aut, "", "")
        lib.agregar_autor(a)
    biblio.registrar_libro(lib)
    return {"mensaje": "Libro registrado", "libro": lib.to_dict()}

@app.put("/api/libros/{codigo}")
def actualizar_libro(codigo: int, req: LibroUpdate):
    try:
        lib = biblio.actualizar_libro(codigo, req.model_dump(exclude_unset=True))
        return {"mensaje": "Libro actualizado", "libro": lib.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/buscar")
def buscar_libro(codigo: int):
    libro = biblio.buscar_libro(codigo)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"libro": libro.to_dict()}

# --- Endpoints Usuarios ---
@app.get("/api/usuarios")
def get_usuarios():
    usuarios = biblio.listar_usuarios()
    return {"usuarios": [u.to_dict() for u in usuarios]}

@app.post("/api/usuarios")
def crear_usuario(req: UsuarioCreate):
    u = Usuario(req.codigo, req.nombre, req.direccion, req.telefono)
    biblio.registrar_usuario(u)
    return {"mensaje": "Usuario registrado", "usuario": u.to_dict()}

@app.put("/api/usuarios/{codigo}")
def actualizar_usuario(codigo: int, req: UsuarioUpdate):
    try:
        u = biblio.actualizar_usuario(codigo, req.model_dump(exclude_unset=True))
        return {"mensaje": "Usuario actualizado", "usuario": u.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- Endpoints Préstamos ---
@app.get("/api/prestamos")
def get_prestamos():
    prestamos = biblio.listar_prestamos()
    return {"prestamos": [p.to_dict() for p in prestamos]}

@app.post("/api/prestamos")
def crear_prestamo(req: PrestamoCreate):
    try:
        p = biblio.realizar_prestamo(req.codigo_usuario, req.codigos_libros, req.fecha_pres)
        return {"mensaje": "Préstamo registrado", "prestamo": p.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/prestamos/{numero_pres}")
def actualizar_prestamo(numero_pres: int, req: PrestamoUpdate):
    try:
        p = biblio.actualizar_prestamo(numero_pres, req.model_dump(exclude_unset=True))
        return {"mensaje": "Préstamo actualizado", "prestamo": p.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/prestamos/devolver/{numero_pres}")
def devolver_prestamo(numero_pres: int):
    try:
        p = biblio.devolver_prestamo(numero_pres)
        return {"mensaje": "Devolución registrada", "prestamo": p.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Servir Frontend
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
    
    @app.exception_handler(404)
    async def custom_404_handler(request, __):
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    print(f"Advertencia: Directorio frontend no encontrado en {frontend_dist}")

