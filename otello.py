import juegos_simplificado as js

class Otello(js.JuegoZT2):

    def __init__(self):
        self.movimientos = [(-1,-1), (-1,0), (-1,1),
                            ( 0,-1),         ( 0,1),
                            ( 1,-1), ( 1,0), ( 1,1)]

    def inicializa(self):
        s = [0] * 64
        s[27], s[28], s[35], s[36] = -1, 1, 1, -1
        return tuple(s)

    def pos(self, fila, columna):
        return fila * 8 + columna

    def dentro(self, fila, columna):
        return 0 <= fila < 8 and 0 <= columna < 8

    def hay_captura(self, s, fila, columna, df, dc, j):
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
        return 0 not in s or (self.jugadas_legales(s, 1) == [None] and self.jugadas_legales(s, -1) == [None])

    def ganancia(self, s):
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

if __name__ == "__main__":
    juego = Otello()
    s = juego.inicializa()

    print("Estado inicial:")
    print(s)

    fila = 2
    columna = 3
    j = 1

    print("\nProbando captura en (2,3) para jugador 1:")
    for df, dc in juego.movimientos:
        print(df, dc, "->", juego.hay_captura(s, fila, columna, df, dc, j))

    juego.imprimir_tablero(s)
