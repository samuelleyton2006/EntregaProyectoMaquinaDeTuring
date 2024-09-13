class Estado:
        def __init__(self, nombre):
            self.nombre = nombre

        def __str__(self):
            return self.nombre  # Para mostrar el nombre del estado

class Transicion:
        def __init__(self, estado_actual, leer_simbolo, simbolo_para_escribir, direccion, siguiente_estado):
            self.estado_actual = estado_actual  # El estado actual ahora es un objeto Estado
            self.leer_simbolo = leer_simbolo
            self.simbolo_para_escribir = simbolo_para_escribir
            self.direccion = direccion  # 1 para derecha, -1 para izquierda
            self.siguiente_estado = siguiente_estado  # El siguiente estado es un objeto Estado

class Cinta:
        def __init__(self, entrada, simbolo_blanco):
            self.cinta = list(entrada) + [simbolo_blanco]
            self.simbolo_blanco = simbolo_blanco

        def leer(self, posicion):
            if posicion >= len(self.cinta):
                return self.simbolo_blanco
            return self.cinta[posicion]

        def escribir(self, posicion, simbolo):
            if posicion >= len(self.cinta):
                self.cinta.append(self.simbolo_blanco)
            self.cinta[posicion] = simbolo

        def __str__(self):
            return ''.join(self.cinta)

class MaquinaTuring:
        def __init__(self, entrada, simbolo_blanco, transiciones):
            self.cinta = Cinta(entrada, simbolo_blanco)
            self.posicion_cabeza = 0
            self.estado = Estado('q0')  # Estado inicial encapsulado en un objeto Estado
            self.transiciones = transiciones
            self.simbolo_blanco = simbolo_blanco

        def encontrar_transicion(self, estado_actual, simbolo_actual):
            for transicion in self.transiciones:
                if transicion.estado_actual.nombre == estado_actual and transicion.leer_simbolo == simbolo_actual:
                    return transicion
            return None

        def ejecutar(self):
            while self.estado.nombre != 'accept' and self.estado.nombre != 'reject':
                self.imprimir_estado_actual()

                simbolo_actual = self.cinta.leer(self.posicion_cabeza)
                transicion = self.encontrar_transicion(self.estado.nombre, simbolo_actual)

                if not transicion:
                    self.estado = Estado('reject')
                    self.imprimir_estado_actual()
                    return

                # Escribir en la cinta
                self.cinta.escribir(self.posicion_cabeza, transicion.simbolo_para_escribir)

                # Mover la cabeza
                self.posicion_cabeza += transicion.direccion

                # Modificar el estado
                self.estado = transicion.siguiente_estado

            self.imprimir_estado_actual()
            if self.estado.nombre == 'accept':
                print("La cadena es aceptada.")
            else:
                print("La cadena es rechazada.")

        def imprimir_estado_actual(self):
            cinta_con_cabeza = list(self.cinta.cinta)
            cinta_con_cabeza.insert(self.posicion_cabeza, '|')
            print(f"Estado: {self.estado}")
            print(f"Cinta: {''.join(cinta_con_cabeza)}")
            print(f"Posición de la cabeza: {self.posicion_cabeza}")
            print("------------------------------")


    # Definir los estados
estado_q0 = Estado('q0')
estado_q1 = Estado('q1')
estado_q2 = Estado('q2')
estado_q3 = Estado('q3')
estado_accept = Estado('accept')

    # Definir las transiciones con objetos Estado
transiciones = [
        Transicion(estado_q0, '0', 'X', 1, estado_q1),
        Transicion(estado_q1, '0', '0', 1, estado_q1),
        Transicion(estado_q1, '1', 'Y', 1, estado_q2),
        Transicion(estado_q2, '0', '0', -1, estado_q2),
        Transicion(estado_q2, 'X', 'X', 1, estado_q0),
        Transicion(estado_q0, 'Y', 'Y', 1, estado_q3),
        Transicion(estado_q3, 'Y', 'Y', 1, estado_q3),
        Transicion(estado_q3, ' ', ' ', 0, estado_accept),
        Transicion(estado_q0, ' ', ' ', 0, estado_accept)
    ]

    # Crear instancia de la Máquina de Turing y ejecutar
mt = MaquinaTuring("01011", ' ', transiciones)
mt.ejecutar()
