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

    def imprimir_tablero(self, s):
        for i in range(8):
            fila = s[i*8:(i+1)*8]
            print(fila)

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
