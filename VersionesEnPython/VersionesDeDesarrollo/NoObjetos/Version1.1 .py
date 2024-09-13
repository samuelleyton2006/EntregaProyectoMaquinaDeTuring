class Caracter:
    VACIO = ' '
    CERO = '0'
    UNO = '1'

class EstadoActual:
    def __init__(self, cinta, posicion_cabezal, estado_maquina):
        self.cinta = cinta
        self.posicion_cabezal = posicion_cabezal
        self.estado_maquina = estado_maquina

class Transiciones:
    def __init__(self, reglas):
        self.reglas = reglas

    def buscar_transicion(self, estado, caracter):
        indice_caracter = 1 if caracter == Caracter.UNO else 0
        return self.reglas[estado][indice_caracter]

class Banda:
    def __init__(self, datos_entrada, longitud=200):
        self.longitud = longitud
        self.banda = [Caracter.VACIO] * (len(datos_entrada) + self.longitud)
        for indice, simbolo in enumerate(datos_entrada):
            self.banda[indice] = simbolo

    def leer_caracter(self, posicion):
        return self.banda[posicion]

    def escribir_caracter(self, posicion, simbolo):
        self.banda[posicion] = simbolo

    def __str__(self):
        return ''.join(self.banda).strip()

class Posicionador:
    def __init__(self, inicio=0):
        self.posicion = inicio

    def mover_cabezal(self, direccion):
        self.posicion += direccion

    def obtener_posicion(self):
        return self.posicion

class ComputadorTuring:
    MAX_PASOS = 10000

    def __init__(self):
        self.transiciones_suma = Transiciones([
            [[0, Caracter.CERO, 1], [0, Caracter.UNO, 1]],
            [[1, Caracter.CERO, -1], [2, Caracter.UNO, -1]],
            [[2, Caracter.UNO, -1], [1, Caracter.CERO, -1]],
            [[1, Caracter.UNO, -1], [2, Caracter.CERO, -1]],
            [[3, Caracter.VACIO, 1], [3, Caracter.VACIO, 1]],
            [[4, Caracter.VACIO, 0], [4, Caracter.VACIO, 0]]
        ])
        # Similar definición para otras operaciones (resta, multiplicación, división)

    def preparar_computador(self, datos):
        return EstadoActual(Banda(datos), Posicionador(), 0)

    def mostrar_cinta(self, maquina):
        print("Banda: ", end="")
        inicio = max(0, maquina.posicion_cabezal.obtener_posicion() - 20)
        fin = min(len(maquina.cinta.banda), maquina.posicion_cabezal.obtener_posicion() + 21)
        for i in range(inicio, fin):
            if i == maquina.posicion_cabezal.obtener_posicion():
                print(f"[{maquina.cinta.leer_caracter(i) if maquina.cinta.leer_caracter(i) != Caracter.VACIO else '_'}]", end="")
            else:
                print(maquina.cinta.leer_caracter(i) if maquina.cinta.leer_caracter(i) != Caracter.VACIO else '_', end="")
        print(f"\nPosición de la cabeza: {maquina.posicion_cabezal.obtener_posicion()}, Estado: {maquina.estado_maquina}")

    def procesar_operacion(self, maquina, reglas_transicion, num_estados):
        pasos = 0
        while maquina.estado_maquina < num_estados - 1 and pasos < self.MAX_PASOS:
            simbolo_actual = maquina.cinta.leer_caracter(maquina.posicion_cabezal.obtener_posicion())
            if simbolo_actual == Caracter.VACIO:
                break

            nuevo_estado, nuevo_simbolo, direccion = reglas_transicion.buscar_transicion(maquina.estado_maquina, simbolo_actual)

            maquina.cinta.escribir_caracter(maquina.posicion_cabezal.obtener_posicion(), nuevo_simbolo)
            maquina.posicion_cabezal.mover_cabezal(direccion)
            maquina.estado_maquina = nuevo_estado

            pasos += 1

        if pasos >= self.MAX_PASOS:
            print("Advertencia: Se alcanzó el límite máximo de pasos.")

# Similarmente, se modifican las demás partes del código
