def congruencia_linear(x0, a, m, c, n):
    """
    Argumentos:
    x0: Semente inicial (int)
    a: Multiplicador (int)
    m: Módulo (int)
    c: Incremento (int)
    n: Número de números a serem gerados (int)

    Retorno:
    Lista de números pseudoaleatórios (float)
    """
    numeros = []
    for _ in range(n):
        xi = ((a * x0) + c) % m
        x0 = xi
        numeros.append(xi / m)
    return numeros


# Parâmetros glibc (gcc)
x0 = 12345  # Semente inicial
a = 1103515245  # Multiplicador
m = 2**31  # Módulo
c = 12345  # Incremento
n = 1000  # Número de números

# Gerando sequência
numeros = congruencia_linear(x0, a, m, c, n)


def gerar_aleatorios(n=1000):
    return congruencia_linear(x0, a, m, c, n)
