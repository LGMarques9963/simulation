class Fila:
    def __init__(self, capacidade=None, servidores=1, min_chegada=None, max_chegada=None, min_saida=None, max_saida=None):
        self.capacidade = capacidade
        self.servidores = servidores
        self.min_chegada = min_chegada
        self.max_chegada = max_chegada
        self.min_saida = min_saida
        self.max_saida = max_saida
        self.status = 0
        self.perdas = 0

    def chegada(self):
        self.status += 1

    def saida(self):
        self.status -= 1

    def gera_saida(self, aleatorio):
        return aleatorio * (self.max_saida - self.min_saida) + self.min_saida

    def gera_chegada(self, aleatorio):
        return aleatorio * (self.max_chegada - self.min_chegada) + self.min_chegada

    def perda(self):
        self.perdas += 1
