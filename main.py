from fila import Fila
from escalonador import Escalonador
from congruencia_linear import gerar_aleatorios


escalonador = Escalonador()
tempo = 0
status1 = []
status2 = []


def acumula_tempo(ev, fila):
    global tempo
    delta_t = ev['tempo'] - tempo
    tempo = ev['tempo']
    status1[fila.status] += delta_t


def acumula_tempo_tandem(ev, fila1, fila2):
    global tempo
    delta_t = ev['tempo'] - tempo
    tempo = ev['tempo']
    status1[fila1.status] += delta_t
    status2[fila2.status] += delta_t


def chegada(ev, aleatorios, fila):
    acumula_tempo(ev, fila)
    if fila.status < fila.capacidade:
        fila.chegada()
        if fila.status <= fila.servidores:
            escalonador.agenda({'tipo': 'saida', 'tempo': (fila.gera_saida(aleatorios.pop(0))) + tempo})
    else:
        fila.perda()
    escalonador.agenda({'tipo': 'chegada', 'tempo': (fila.gera_chegada(aleatorios.pop(0))) + tempo})


def chegada_tandem(ev, aleatorios, fila1, fila2):
    acumula_tempo_tandem(ev, fila1, fila2)
    if fila1.status < fila1.capacidade:
        fila1.chegada()
        if fila1.status <= fila1.servidores:
            escalonador.agenda({'tipo': 'passagem', 'tempo': (fila1.gera_saida(aleatorios.pop(0))) + tempo})
    else:
        fila1.perda()
    escalonador.agenda({'tipo': 'chegada', 'tempo': (fila1.gera_chegada(aleatorios.pop(0))) + tempo})


def saida(ev, aleatorios, fila):
    acumula_tempo(ev, fila)
    fila.saida()
    if fila.status >= fila.servidores:
        escalonador.agenda({'tipo': 'saida', 'tempo': (fila.gera_saida(aleatorios.pop(0))) + tempo})


def saida_tandem(ev, aleatorios, fila1, fila2):
    acumula_tempo_tandem(ev, fila1, fila2)
    fila2.saida()
    if fila2.status >= fila2.servidores:
        escalonador.agenda({'tipo': 'saida', 'tempo': (fila2.gera_saida(aleatorios.pop(0))) + tempo})


def passagem(ev, aleatorios, fila1, fila2):
    acumula_tempo_tandem(ev, fila1, fila2)
    fila1.saida()
    if fila1.status >= fila1.servidores:
        escalonador.agenda({'tipo': 'passagem', 'tempo': (fila1.gera_saida(aleatorios.pop(0))) + tempo})
    if fila2.status < fila2.capacidade:
        fila2.chegada()
        if fila2.status <= fila2.servidores:
            escalonador.agenda({'tipo': 'saida', 'tempo': (fila2.gera_saida(aleatorios.pop(0))) + tempo})
    else:
        fila2.perda()


def simula_fila_unica():
    global status1, escalonador, tempo

    fila1 = Fila(capacidade=5, servidores=1, min_chegada=2, max_chegada=5, min_saida=3, max_saida=5)
    fila2 = Fila(capacidade=5, servidores=2, min_chegada=2, max_chegada=5, min_saida=3, max_saida=5)
    
    aleatorios1 = gerar_aleatorios(100000)
    aleatorios2 = aleatorios1.copy()

    print("\nFila 1 (G/G/1/5):")
    status1.clear()
    status1 = [0 for _ in range(fila1.capacidade + 1)]
    tempo = 0
    escalonador = Escalonador()
    escalonador.agenda({'tipo': 'chegada', 'tempo': 2})
    while len(aleatorios1) > 0:
        ev = escalonador.avaliar()
        if ev['tipo'] == 'chegada':
            chegada(ev, aleatorios1, fila1)
        else:
            saida(ev, aleatorios1, fila1)
    print('Tempo total:', tempo)
    print('Status:', status1)
    print('Probabilidades:', [s / tempo for s in status1])
    print('Perdas:', fila1.perdas)

    print("\nFila 2 (G/G/2/5):")
    status1.clear()
    status1 = [0 for _ in range(fila2.capacidade + 1)]
    tempo = 0
    escalonador = Escalonador()
    escalonador.agenda({'tipo': 'chegada', 'tempo': 2})
    while len(aleatorios2) > 0:
        ev = escalonador.avaliar()
        if ev['tipo'] == 'chegada':
            chegada(ev, aleatorios2, fila2)
        else:
            saida(ev, aleatorios2, fila2)
    print('Tempo total:', tempo)
    print('Status:', status1)
    print('Probabilidades:', [s / tempo for s in status1])
    print('Perdas:', fila2.perdas)


def simula_filas_tandem():
    global status1, status2, escalonador, tempo

    fila1 = Fila(capacidade=3, servidores=2, min_chegada=1, max_chegada=4, min_saida=3, max_saida=4)
    fila2 = Fila(capacidade=5, servidores=1, min_saida=2, max_saida=3)
    
    aleatorios = gerar_aleatorios(100000)

    print("\nFila 1 (G/G/2/3) e Fila 2 (G/G/1/5) em tandem:")
    status1.clear()
    status2.clear()
    status1 = [0 for _ in range(fila1.capacidade + 1)]
    status2 = [0 for _ in range(fila2.capacidade + 1)]
    tempo = 0
    escalonador = Escalonador()
    escalonador.agenda({'tipo': 'chegada', 'tempo': 1.5})
    while len(aleatorios) > 0:
        ev = escalonador.avaliar()
        if ev['tipo'] == 'chegada':
            chegada_tandem(ev, aleatorios, fila1, fila2)
        elif ev['tipo'] == 'saida':
            saida_tandem(ev, aleatorios, fila1, fila2)
        else:
            passagem(ev, aleatorios, fila1, fila2)
            
    print("\nFila 1 (G/G/2/3):")
    print('Tempo total:', tempo)
    print('Status:', status1)
    print('Probabilidades:', [s / tempo for s in status1])
    print('Perdas:', fila1.perdas)
    
    print("\nFila 2 (G/G/1/5):")
    print('Tempo total:', tempo)
    print('Status:', status2)
    print('Probabilidades:', [s / tempo for s in status2])
    print('Perdas:', fila2.perdas)

#simula_fila_unica()
simula_filas_tandem()
