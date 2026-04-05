class NodoArbol:
    def __init__(self, clave, valor):
        self.clave = clave      # El codigo_lib será la clave
        self.valor = valor      # El objeto Libro será el valor
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, clave, valor):
        if self.raiz is None:
            self.raiz = NodoArbol(clave, valor)
        else:
            self._insertar_recursivo(self.raiz, clave, valor)

    def _insertar_recursivo(self, nodo_actual, clave, valor):
        if clave < nodo_actual.clave:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = NodoArbol(clave, valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, clave, valor)
        elif clave > nodo_actual.clave:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = NodoArbol(clave, valor)
            else:
                self._insertar_recursivo(nodo_actual.derecho, clave, valor)
        else:
            # Si la clave ya existe, se actualiza el valor (o se podría manejar como error)
            nodo_actual.valor = valor

    def buscar(self, clave):
        return self._buscar_recursivo(self.raiz, clave)

    def _buscar_recursivo(self, nodo_actual, clave):
        if nodo_actual is None:
            return None
        if nodo_actual.clave == clave:
            return nodo_actual.valor
        elif clave < nodo_actual.clave:
            return self._buscar_recursivo(nodo_actual.izquierdo, clave)
        else:
            return self._buscar_recursivo(nodo_actual.derecho, clave)

    def recorrido_inorden(self):
        resultado = []
        self._recorrido_inorden_recursivo(self.raiz, resultado)
        return resultado

    def _recorrido_inorden_recursivo(self, nodo_actual, resultado):
        if nodo_actual is not None:
            self._recorrido_inorden_recursivo(nodo_actual.izquierdo, resultado)
            resultado.append(nodo_actual.valor)
            self._recorrido_inorden_recursivo(nodo_actual.derecho, resultado)
