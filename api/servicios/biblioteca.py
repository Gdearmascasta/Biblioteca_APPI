from estructuras.arbol_bst import ArbolBinarioBusqueda
from estructuras.tabla_hash import TablaHash
from estructuras.lista_enlazada import ListaEnlazada
from modelos.entidades import Prestamo

class Biblioteca:
    def __init__(self):
        self.catalogo_libros = ArbolBinarioBusqueda()   
        self.usuarios_registrados = TablaHash()         
        self.historial_prestamos = ListaEnlazada()      
        
        self.autores = []
        self.editoriales = []
        self.nacionalidades = []
        self.contador_prestamos = 1

    def registrar_libro(self, libro):
        self.catalogo_libros.insertar(libro.codigo_lib, libro)
        return libro

    def buscar_libro(self, codigo_lib):
        return self.catalogo_libros.buscar(codigo_lib)

    def listar_libros(self):
        return self.catalogo_libros.recorrido_inorden()

    def registrar_usuario(self, usuario):
        self.usuarios_registrados.insertar(usuario.codigo_usu, usuario)
        return usuario

    def buscar_usuario(self, codigo_usu):
        return self.usuarios_registrados.buscar(codigo_usu)
        
    def listar_usuarios(self):
        return self.usuarios_registrados.obtener_todos()

    def actualizar_libro(self, codigo_lib, datos_nuevos):
        libro = self.buscar_libro(codigo_lib)
        if not libro:
            raise ValueError(f"Libro {codigo_lib} no encontrado")
        
        if "titulo" in datos_nuevos:
            libro.nombre_lib = datos_nuevos["titulo"]
        if "editorial_nombre" in datos_nuevos:
            libro.editorial.nombre_edi = datos_nuevos["editorial_nombre"]
        if "autores_nombres" in datos_nuevos:
            from modelos.entidades import Autor
            libro.autores = []
            for n_aut in datos_nuevos["autores_nombres"]:
                a = Autor(100, n_aut, "", "")
                libro.agregar_autor(a)
        return libro

    def actualizar_usuario(self, codigo_usu, datos_nuevos):
        usuario = self.buscar_usuario(codigo_usu)
        if not usuario:
            raise ValueError(f"Usuario {codigo_usu} no encontrado")
        
        if "nombre" in datos_nuevos:
            usuario.nombre_usu = datos_nuevos["nombre"]
        if "direccion" in datos_nuevos:
            usuario.direccion_usu = datos_nuevos["direccion"]
        if "telefono" in datos_nuevos:
            usuario.telefono_usu = datos_nuevos["telefono"]
        return usuario

    def actualizar_prestamo(self, numero_pres, datos_nuevos):
        prestamos = self.historial_prestamos.buscar(lambda p: p.numero_pres == numero_pres)
        if not prestamos:
            raise ValueError(f"Préstamo #{numero_pres} no encontrado.")
        prestamo = prestamos[0]
        
        if "dias_en_mora" in datos_nuevos:
            prestamo.dias_en_mora = datos_nuevos["dias_en_mora"]
            prestamo.valor_multa = prestamo.dias_en_mora * 5000
        return prestamo

    def realizar_prestamo(self, codigo_usu, codigos_libros, fecha_pres_str=None):
        usuario = self.buscar_usuario(codigo_usu)
        if not usuario:
            raise ValueError(f"Usuario {codigo_usu} no encontrado")

        nuevo_prestamo = Prestamo(self.contador_prestamos, codigo_usu, 0)
        
        if fecha_pres_str:
            from datetime import datetime
            try:
                nuevo_prestamo.fecha_pres = datetime.strptime(fecha_pres_str, "%Y-%m-%d")
            except ValueError:
                pass
                
        libros_agregados = 0
        for cod in codigos_libros:
            libro = self.buscar_libro(cod)
            if libro:
                nuevo_prestamo.agregar_libro(libro)
                libros_agregados += 1

        if libros_agregados > 0:
            self.historial_prestamos.agregar_al_final(nuevo_prestamo)
            self.contador_prestamos += 1
            return nuevo_prestamo
        else:
            raise ValueError("Ningún libro válido proporcionado.")

    def devolver_prestamo(self, numero_pres, fecha_ent_real=None):
        prestamos = self.historial_prestamos.buscar(lambda p: p.numero_pres == numero_pres)
        
        if prestamos:
            prestamo = prestamos[0]
            if prestamo.fecha_ent_real is None:
                prestamo.devolver(fecha_ent_real)
                return prestamo
            else:
                raise ValueError(f"El préstamo #{numero_pres} ya está devuelto.")
        else:
            raise ValueError(f"Préstamo #{numero_pres} no encontrado.")

    def listar_prestamos(self):
        return self.historial_prestamos.obtener_todos()
