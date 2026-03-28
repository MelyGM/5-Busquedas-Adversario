import juegos_simplificado as js
import minimax

class Otello(js.JuegoZT2):
    """
    Clase que define la lógica del juego Otello.
    Hereda de JuegoZT2.
    """

    def __init__(self):
        """
        Define las direcciones posibles en el tablero:
        horizontales, verticales y diagonales.
        """
        self.movimientos = [(-1,-1), (-1,0), (-1,1),
                            ( 0,-1),         ( 0,1),
                            ( 1,-1), ( 1,0), ( 1,1)]

    def inicializa(self):
        """
        Crea el estado inicial del tablero (8x8).

        Se representa como una tupla de 64 posiciones:
        - 0: vacío
        - 1: jugador 1 (X)
        - -1: jugador 2 (O)

        Se colocan las 4 fichas iniciales en el centro.
        """
        s = [0] * 64
        s[27], s[28], s[35], s[36] = -1, 1, 1, -1
        return tuple(s)

    def pos(self, fila, columna):
        """
        Convierte coordenadas (fila, columna)
        a índice lineal del tablero.
        """
        return fila * 8 + columna

    def dentro(self, fila, columna):
        """
        Verifica si una posición está dentro del tablero.
        """
        return 0 <= fila < 8 and 0 <= columna < 8

    def hay_captura(self, s, fila, columna, df, dc, j):
        """
        Verifica si al colocar una ficha en una dirección
        se capturan fichas del rival.

        - df, dc: dirección
        - j: jugador actual

        Regresa True si hay captura, False en caso contrario.
        """
        fila += df
        columna += dc

        if not self.dentro(fila, columna):
            return False

        if s[self.pos(fila, columna)] != -j:
            return False

        fila += df
        columna += dc

        while self.dentro(fila, columna):
            valor = s[self.pos(fila, columna)]

            if valor == 0:
                return False
            if valor == j:
                return True

            fila += df
            columna += dc

        return False

    def jugadas_legales(self, s, j):
        """
        Regresa todas las jugadas válidas para el jugador j.

        Si no hay jugadas disponibles, regresa [None]
        (indica que el jugador pasa turno).
        """
        jugadas = []

        for a in range(64):
            if s[a] != 0:
                continue

            fila = a // 8
            columna = a % 8

            for df, dc in self.movimientos:
                if self.hay_captura(s, fila, columna, df, dc, j):
                    jugadas.append(a)
                    break

        return jugadas if jugadas else [None]

    def sucesor(self, s, a, j):
        """
        Genera el siguiente estado después de una jugada.

        - Coloca la ficha
        - Voltea las fichas capturadas
        """
        if a is None:
            return s

        s = list(s)
        s[a] = j

        fila = a // 8
        columna = a % 8

        for df, dc in self.movimientos:
            if self.hay_captura(tuple(s), fila, columna, df, dc, j):
                f = fila + df
                c = columna + dc

                while self.dentro(f, c) and s[self.pos(f, c)] == -j:
                    s[self.pos(f, c)] = j
                    f += df
                    c += dc

        return tuple(s)

    def terminal(self, s):
        """
        Determina si el juego terminó.

        El juego termina cuando:
        - No hay espacios vacíos, o
        - Ningún jugador tiene jugadas legales
        """
        return 0 not in s or (self.jugadas_legales(s, 1) == [None] and self.jugadas_legales(s, -1) == [None])

    def ganancia(self, s):
        """
        Calcula el resultado del juego:

        1  -> gana jugador 1
        -1 -> gana jugador 2
        0  -> empate
        """
        j1 = s.count(1)
        j2 = s.count(-1)

        if j1 > j2:
            return 1
        elif j2 > j1:
            return -1
        return 0

    def imprimir_tablero(self, s):
        print("\n   ", end="")
        for c in range(8):
            print(c, end=" ")
        print("\n")

        for f in range(8):
            print(f, end="  ")
            for c in range(8):
                val = s[self.pos(f, c)]

                if val == 1:
                    print("X", end=" ")
                elif val == -1:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            print()

class InterfaceOtello(js.JuegoInterface):
    """
    Interfaz de consola para jugar Otello.
    Permite interacción entre jugador humano y la IA.
    """
    def muestra_estado(self, s):
        print("\nEstado actual del tablero:")
        self.juego.imprimir_tablero(s)

    def muestra_ganador(self, g):
        print("\nResultado final:")

        if g == 1:
            print("Gana jugador X (negras)")
        elif g == -1:
            print("Gana jugador O (blancas)")
        else:
            print("Empate")

    def jugador_humano(self, s, j):
        """
        Permite al usuario ingresar jugadas desde consola.

        - Muestra jugadas posibles
        - Valida la entrada
        """
        print("\nTurno del jugador:", "X" if j == 1 else "O")

        jugadas = self.juego.jugadas_legales(s,j)

        if jugadas == [None]:
            print("No hay jugadas disponibles. Se pasa turno.")
            input("Presiona ENTER para continuar...")
            return None
        
        print("Jugadas posibles:")

        for a in jugadas:
            f = a // 8
            c = a % 8
            print(f"{a} -> ({f},{c})")

        while True:
            entrada = input("Elige una jugada (número):")

            try:
                a = int(entrada)
                if a in jugadas:
                    return a
                else:
                    print("Jugada inválida.")
            except ValueError:
                print("Entrada inválida.")

def ordena_otello(jugadas, jugador):
    """
    Ordena las jugadas para mejorar la búsqueda.

    Prioridad:
    1. Esquinas (más importantes)
    2. Bordes
    3. Otras jugadas
    """
    esquinas = [0, 7, 56, 63]
    bordes = [
        1, 2, 3, 4, 5, 6,
        8, 16, 24, 32, 40, 48,
        15, 23, 31, 39, 47, 55,
        57, 58, 59, 60, 61, 62
    ]

    jugadas_ordenadas = []
    otras = []

    for a in jugadas:
        if a is None:
            otras.append(a)
        elif a in esquinas:
            jugadas_ordenadas.append(a)

    for a in jugadas:
        if a is not None and a not in jugadas_ordenadas and a in bordes:
            jugadas_ordenadas.append(a)

    for a in jugadas:
        if a not in jugadas_ordenadas:
            otras.append(a)

    return jugadas_ordenadas + otras

def evalua_otello(s):
    """
    Evalúa el estado del tablero.

    Factores considerados:
    - Diferencia de fichas
    - Control de esquinas
    - Control de bordes

    Se asignan pesos a cada característica.
    Regresa un valor entre -1 y 1.
    """
    esquinas = [0, 7, 56, 63]
    bordes = [
        1, 2, 3, 4, 5, 6,
        8, 16, 24, 32, 40, 48,
        15, 23, 31, 39, 47, 55,
        57, 58, 59, 60, 61, 62
    ]

    fichas_j1 = s.count(1)
    fichas_j2 = s.count(-1)

    valor_fichas = fichas_j1 - fichas_j2

    esquinas_j1 = 0
    esquinas_j2 = 0
    for e in esquinas:
        if s[e] == 1:
            esquinas_j1 += 1
        elif s[e] == -1:
            esquinas_j2 += 1

    valor_esquinas = esquinas_j1 - esquinas_j2

    bordes_j1 = 0
    bordes_j2 = 0
    for b in bordes:
        if s[b] == 1:
            bordes_j1 += 1
        elif s[b] == -1:
            bordes_j2 += 1

    valor_bordes = bordes_j1 - bordes_j2

    valor = 2 * valor_fichas + 10 * valor_esquinas + 4 * valor_bordes

    if valor > 100:
        valor = 100
    if valor < -100:
        valor = -100

    return valor / 100

if __name__ == "__main__":

    cfg = {
        "Jugador 1": "Humano",
        "Jugador 2": "Negamax",  
    }

    def jugador_cfg(tipo):
        if tipo == "Humano":
            return "Humano"
        elif tipo == "Aleatorio":
            return js.JugadorAleatorio()
        elif tipo == "Negamax":
            return minimax.JugadorNegamax(
                ordena=ordena_otello,
                d=5,
                evalua=evalua_otello
            )
        else:
            raise ValueError("Jugador no válido")

    interfaz = InterfaceOtello(
        Otello(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("JUEGO OTHELLO")
    print("Jugador 1:", cfg["Jugador 1"])
    print("Jugador 2:", cfg["Jugador 2"])

    interfaz.juega()
