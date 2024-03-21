from fila import Fila
from escalonador import Escalonador
from congruencia_linear import gerar_aleatorios

fila1 = Fila(capacidade=5, servidores=1, min_chegada=2, max_chegada=5, min_saida=3, max_saida=5)
fila2 = Fila(capacidade=5, servidores=2, min_chegada=2, max_chegada=5, min_saida=3, max_saida=5)
escalonador = Escalonador()
tempo = 0
aleatorios1 = gerar_aleatorios(100000)
aleatorios2 = aleatorios1.copy()
status = [0 for _ in range(fila1.capacidade + 1)]


def acumula_tempo(ev):
    global tempo
    delta_t = ev['tempo'] - tempo
    tempo = ev['tempo']
    status[fila1.status] += delta_t


def chegada(ev, fila, aleatorios1=aleatorios1):
    acumula_tempo(ev)
    if fila.status < fila.capacidade:
        fila.chegada()
        if fila.status <= fila.servidores:
            escalonador.agenda({'tipo': 'saida', 'tempo': (fila.gera_saida(aleatorios1.pop(0))) + tempo})
    else:
        fila.perda()
    escalonador.agenda({'tipo': 'chegada', 'tempo': (fila.gera_chegada(aleatorios1.pop(0))) + tempo})


def saida(ev, fila, aleatorios1=aleatorios1):
    acumula_tempo(ev)
    fila.saida()
    if fila.status >= fila.servidores:
        escalonador.agenda({'tipo': 'saida', 'tempo': (fila.gera_saida(aleatorios1.pop(0))) + tempo})


print("Fila 1 (G/G/1/5):")
escalonador.agenda({'tipo': 'chegada', 'tempo': 2})
while len(aleatorios1) > 0:
    ev = escalonador.avaliar()
    if ev['tipo'] == 'chegada':
        chegada(ev, fila1)
    else:
        saida(ev, fila1)
print('Tempo total:', tempo)
print('Status:', status)
print('Probabilidades:', [s / tempo for s in status])
print('Perdas:', fila1.perdas)

print("\n\n\n")

print("Fila 2 (G/G/2/5):")
escalonador = Escalonador()
escalonador.agenda({'tipo': 'chegada', 'tempo': 2})
while len(aleatorios2) > 0:
    ev = escalonador.avaliar()
    if ev['tipo'] == 'chegada':
        chegada(ev, fila2, aleatorios2)
    else:
        saida(ev, fila2, aleatorios2)
print('Tempo total:', tempo)
print('Status:', status)
print('Probabilidades:', [s / tempo for s in status])
print('Perdas:', fila2.perdas)
