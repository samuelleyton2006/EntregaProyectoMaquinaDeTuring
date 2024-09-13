class Caracter:
    VACIO = ' '
    CERO = '0'
    UNO = '1'

class EstadoActual:
    def __init__(self, banda, posicion_cabezal, estado_maquina):
        self.banda = banda
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
        self.transiciones_resta = Transiciones([
            [[0, Caracter.CERO, 1], [0, Caracter.UNO, 1]],
            [[1, Caracter.CERO, -1], [2, Caracter.UNO, -1]],
            [[2, Caracter.UNO, -1], [1, Caracter.CERO, -1]],
            [[3, Caracter.VACIO, 1], [3, Caracter.VACIO, 1]],
            [[4, Caracter.VACIO, 0], [4, Caracter.VACIO, 0]]
        ])
        # Similar definición para multiplicación y división (no incluida para brevedad)

    def preparar_computador(self, datos):
        return EstadoActual(Banda(datos), Posicionador(), 0)

    def mostrar_cinta(self, maquina):
        print("Banda: ", end="")
        inicio = max(0, maquina.posicion_cabezal.obtener_posicion() - 20)
        fin = min(len(maquina.banda.banda), maquina.posicion_cabezal.obtener_posicion() + 21)
        for i in range(inicio, fin):
            if i == maquina.posicion_cabezal.obtener_posicion():
                print(f"[{maquina.banda.leer_caracter(i) if maquina.banda.leer_caracter(i) != Caracter.VACIO else '_'}]", end="")
            else:
                print(maquina.banda.leer_caracter(i) if maquina.banda.leer_caracter(i) != Caracter.VACIO else '_', end="")
        print(f"\nPosición de la cabeza: {maquina.posicion_cabezal.obtener_posicion()}, Estado: {maquina.estado_maquina}")

    def procesar_operacion(self, maquina, reglas_transicion, num_estados):
        pasos = 0
        while maquina.estado_maquina < num_estados - 1 and pasos < self.MAX_PASOS:
            simbolo_actual = maquina.banda.leer_caracter(maquina.posicion_cabezal.obtener_posicion())
            if simbolo_actual == Caracter.VACIO:
                break

            nuevo_estado, nuevo_simbolo, direccion = reglas_transicion.buscar_transicion(maquina.estado_maquina, simbolo_actual)

            maquina.banda.escribir_caracter(maquina.posicion_cabezal.obtener_posicion(), nuevo_simbolo)
            maquina.posicion_cabezal.mover_cabezal(direccion)
            maquina.estado_maquina = nuevo_estado

            pasos += 1

        if pasos >= self.MAX_PASOS:
            print("Advertencia: Se alcanzó el límite máximo de pasos.")

    def extraer_resultado_binario(self, banda):
        resultado = ''
        encontrado_uno = False
        for simbolo in banda.banda:
            if simbolo in [Caracter.CERO, Caracter.UNO]:
                if simbolo == Caracter.UNO:
                    encontrado_uno = True
                if encontrado_uno:
                    resultado += simbolo
        return resultado if resultado else None

class Operacion:
    SUMA = '+'
    RESTA = '-'

    @staticmethod
    def es_valida(op):
        return op in [Operacion.SUMA, Operacion.RESTA]

    @staticmethod
    def realizar(num1, num2, op):
        if op == Operacion.SUMA:
            return num1 + num2
        elif op == Operacion.RESTA:
            return num1 - num2

class EntradaUsuario:
    @staticmethod
    def obtener_numeros_binarios():
        while True:
            entrada = input("Ingrese dos números binarios separados por un espacio: ")
            if EntradaUsuario.es_binario_valido(entrada):
                return entrada.split()
            print("Error: La entrada debe contener solo '0', '1' y espacios.")

    @staticmethod
    def obtener_operacion():
        while True:
            operacion = input("Ingrese la operación (+, -): ")
            if Operacion.es_valida(operacion):
                return operacion
            print("Error: Operación no reconocida.")

    @staticmethod
    def es_binario_valido(cadena):
        return all(char in '01 ' for char in cadena)

class Aplicacion:
    def __init__(self):
        self.computador_turing = ComputadorTuring()

    def ejecutar(self):
        num1, num2 = EntradaUsuario.obtener_numeros_binarios()
        operacion = EntradaUsuario.obtener_operacion()

        entrada = f"{num1} {num2}"
        maquina = self.computador_turing.preparar_computador(entrada)

        print("Entrada inicial:")
        self.computador_turing.mostrar_cinta(maquina)

        num1_decimal = int(num1, 2)
        num2_decimal = int(num2, 2)

        if operacion == Operacion.SUMA:
            self.computador_turing.procesar_operacion(maquina, self.computador_turing.transiciones_suma, 6)
        elif operacion == Operacion.RESTA:
            if num1_decimal < num2_decimal:
                print("Error: El primer número debe ser mayor o igual al segundo para la resta.")
                return
            self.computador_turing.procesar_operacion(maquina, self.computador_turing.transiciones_resta, 5)

        print(f"\nResultado de la operación {operacion}:")
        self.computador_turing.mostrar_cinta(maquina)

        resultado_binario = self.computador_turing.extraer_resultado_binario(maquina.banda)
        if resultado_binario:
            print(f"\nResultado en binario: {resultado_binario}")
        else:
            print("\nNo se encontró un resultado binario válido en la cinta.")

if __name__ == "__main__":
    app = Aplicacion()
    app.ejecutar()
