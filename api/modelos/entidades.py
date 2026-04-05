from datetime import datetime

class Nacionalidad:
    def __init__(self, codigo_nac, nombre_nac):
        self.codigo_nac = codigo_nac
        self.nombre_nac = nombre_nac

    def to_dict(self):
        return {
            "codigo_nac": self.codigo_nac,
            "nombre_nac": self.nombre_nac
        }

class Autor:
    def __init__(self, codigo_aut, nombre_aut, email_aut, genero_aut, nacionalidad=None):
        self.codigo_aut = codigo_aut
        self.nombre_aut = nombre_aut
        self.email_aut = email_aut
        self.genero_aut = genero_aut
        self.nacionalidad = nacionalidad 

    def to_dict(self):
        return {
            "codigo_aut": self.codigo_aut,
            "nombre_aut": self.nombre_aut,
            "email_aut": self.email_aut,
            "genero_aut": self.genero_aut,
            "nacionalidad": self.nacionalidad.to_dict() if self.nacionalidad else None
        }

class Editorial:
    def __init__(self, codigo_edi, nombre_edi):
        self.codigo_edi = codigo_edi
        self.nombre_edi = nombre_edi

    def to_dict(self):
        return {
            "codigo_edi": self.codigo_edi,
            "nombre_edi": self.nombre_edi
        }

class Libro:
    def __init__(self, codigo_lib, nombre_lib, editorial=None):
        self.codigo_lib = codigo_lib
        self.nombre_lib = nombre_lib
        self.editorial = editorial        
        self.autores = []                 

    def agregar_autor(self, autor):
        self.autores.append(autor)

    def to_dict(self):
        return {
            "codigo_lib": self.codigo_lib,
            "nombre_lib": self.nombre_lib,
            "editorial": self.editorial.to_dict() if self.editorial else None,
            "autores": [a.to_dict() for a in self.autores]
        }

class Usuario:
    def __init__(self, codigo_usu, nombre_usu, direccion_usu, telefono_usu):
        self.codigo_usu = codigo_usu
        self.nombre_usu = nombre_usu
        self.direccion_usu = direccion_usu
        self.telefono_usu = telefono_usu

    def to_dict(self):
        return {
            "codigo_usu": self.codigo_usu,
            "nombre_usu": self.nombre_usu,
            "direccion_usu": self.direccion_usu,
            "telefono_usu": self.telefono_usu
        }

class Prestamo:
    def __init__(self, numero_pres, codigo_usu, fecha_ent_prop):
        self.numero_pres = numero_pres
        self.codigo_usu = codigo_usu                
        self.fecha_pres = datetime.now()
        # Ensure fecha_ent_prop is datetime
        if isinstance(fecha_ent_prop, str):
            try:
                self.fecha_ent_prop = datetime.fromisoformat(fecha_ent_prop)
            except:
                self.fecha_ent_prop = datetime.strptime(fecha_ent_prop, "%Y-%m-%d")
        else:
            self.fecha_ent_prop = fecha_ent_prop
            
        self.fecha_ent_real = None                  
        self.valor_multa = 0.0
        self.libros = []                            

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def devolver(self, fecha_ent_real=None):
        if fecha_ent_real is None:
            self.fecha_ent_real = datetime.now()
        else:
            self.fecha_ent_real = fecha_ent_real
            
        if self.fecha_ent_real > self.fecha_ent_prop:
            dias_retraso = (self.fecha_ent_real - self.fecha_ent_prop).days
            if dias_retraso > 0:
                self.valor_multa = dias_retraso * 5000  

    def to_dict(self):
        return {
            "numero_pres": self.numero_pres,
            "codigo_usu": self.codigo_usu,
            "fecha_pres": self.fecha_pres.isoformat() if self.fecha_pres else None,
            "fecha_ent_prop": self.fecha_ent_prop.isoformat() if self.fecha_ent_prop else None,
            "fecha_ent_real": self.fecha_ent_real.isoformat() if self.fecha_ent_real else None,
            "estado": "DEVUELTO" if self.fecha_ent_real else "ACTIVO",
            "valor_multa": self.valor_multa,
            "libros": [l.to_dict() for l in self.libros]
        }
