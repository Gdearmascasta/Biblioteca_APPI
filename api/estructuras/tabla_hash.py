class NodoHash:
    def __init__(self, clave, valor):
        self.clave = clave      # El codigo_usu
        self.valor = valor      # Objeto Usuario
        self.siguiente = None   # Para encadenamiento en caso de colisión

class TablaHash:
    def __init__(self, tamano=100):
        self.tamano = tamano
        self.tabla = [None] * tamano
        self.num_elementos = 0

    def _hash(self, clave):
        # Una función hash simple basada en el valor de la clave (string o int)
        if isinstance(clave, str):
            h = 0
            for caracter in clave:
                h = (h * 31 + ord(caracter)) % self.tamano
            return h
        elif isinstance(clave, int):
            return clave % self.tamano
        else:
            return hash(clave) % self.tamano

    def insertar(self, clave, valor):
        indice = self._hash(clave)
        
        # Revisar si la clave ya existe para actualizar el valor
        nodo_actual = self.tabla[indice]
        while nodo_actual is not None:
            if nodo_actual.clave == clave:
                nodo_actual.valor = valor
                return
            nodo_actual = nodo_actual.siguiente
            
        # Insertar al inicio de la lista enlazada (encadenamiento)
        nuevo_nodo = NodoHash(clave, valor)
        nuevo_nodo.siguiente = self.tabla[indice]
        self.tabla[indice] = nuevo_nodo
        self.num_elementos += 1
        
        # Redimensionamiento dinámico (factor de carga > 0.7)
        if self.num_elementos / self.tamano > 0.7:
            self._redimensionar()

    def buscar(self, clave):
        indice = self._hash(clave)
        nodo_actual = self.tabla[indice]
        while nodo_actual is not None:
            if nodo_actual.clave == clave:
                return nodo_actual.valor
            nodo_actual = nodo_actual.siguiente
        return None

    def eliminar(self, clave):
        indice = self._hash(clave)
        nodo_actual = self.tabla[indice]
        nodo_anterior = None
        
        while nodo_actual is not None:
            if nodo_actual.clave == clave:
                if nodo_anterior is None:
                    self.tabla[indice] = nodo_actual.siguiente
                else:
                    nodo_anterior.siguiente = nodo_actual.siguiente
                self.num_elementos -= 1
                return True
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente
        return False
        
    def _redimensionar(self):
        nuevo_tamano = self.tamano * 2
        nueva_tabla = [None] * nuevo_tamano
        
        # Mover todos los elementos
        for i in range(self.tamano):
            nodo_actual = self.tabla[i]
            while nodo_actual is not None:
                indice = self._hash(nodo_actual.clave)
                nuevo_nodo = NodoHash(nodo_actual.clave, nodo_actual.valor)
                nuevo_nodo.siguiente = nueva_tabla[indice]
                nueva_tabla[indice] = nuevo_nodo
                nodo_actual = nodo_actual.siguiente
                
        self.tamano = nuevo_tamano
        self.tabla = nueva_tabla

    def obtener_todos(self):
        elementos = []
        for i in range(self.tamano):
            nodo_actual = self.tabla[i]
            while nodo_actual is not None:
                elementos.append(nodo_actual.valor)
                nodo_actual = nodo_actual.siguiente
        return elementos
