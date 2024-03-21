import heapq


class Escalonador:
    def __init__(self):
        self.chegada = []
        self.saida = []
        self.tempo = 0

    def avaliar(self):
        if len(self.chegada) == 0 and len(self.saida) == 0:
            return None
        if len(self.chegada) == 0:
            return {'tipo': 'saida', 'tempo': heapq.heappop(self.saida)}
        if len(self.saida) == 0:
            return {'tipo': 'chegada', 'tempo': heapq.heappop(self.chegada)}
        chega = heapq.heappop(self.chegada)
        sai = heapq.heappop(self.saida)
        if chega < sai:
            heapq.heappush(self.saida, sai)
            return {'tipo': 'chegada', 'tempo': chega}
        else:
            heapq.heappush(self.chegada, chega)
            return {'tipo': 'saida', 'tempo': sai}

    def agenda(self, processo):
        if processo['tipo'] == 'chegada':
            heapq.heappush(self.chegada, processo['tempo'])
        else:
            heapq.heappush(self.saida, processo['tempo'])