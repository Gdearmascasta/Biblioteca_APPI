class NodoLista:
    def __init__(self, valor):
        self.valor = valor      # Objeto Prestamo
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None        # Mantenemos referencia a la cola para inserción O(1) al final
        self.tamano = 0

    def agregar_al_final(self, valor):
        nuevo_nodo = NodoLista(valor)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamano += 1

    def agregar_al_inicio(self, valor):
        nuevo_nodo = NodoLista(valor)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
        self.tamano += 1

    def buscar(self, condicion):
        # La condición es una función lambda que devuelve True si el elemento coincide
        resultados = []
        nodo_actual = self.cabeza
        while nodo_actual is not None:
            if condicion(nodo_actual.valor):
                resultados.append(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente
        return resultados

    def obtener_todos(self):
        elementos = []
        nodo_actual = self.cabeza
        while nodo_actual is not None:
            elementos.append(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente
        return elementos

    def esta_vacia(self):
        return self.cabeza is None

    def __len__(self):
        return self.tamano
