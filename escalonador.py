import heapq


class Escalonador:
    def __init__(self):
        self.chegada = []
        self.passagem = []
        self.saida = []
        self.tempo = 0

    def avaliar(self):
        chega = -1
        if len(self.chegada) > 0:
            chega = heapq.heappop(self.chegada)

        passa = -1
        if len(self.passagem) > 0:
            passa = heapq.heappop(self.passagem)

        sai = -1
        if len(self.saida) > 0:
            sai = heapq.heappop(self.saida)

        if chega != -1 and (passa == -1 or chega < passa) and (sai == -1 or chega < sai):
            if passa != -1:
                heapq.heappush(self.passagem, passa)
            if sai != -1:
                heapq.heappush(self.saida, sai)
            return {'tipo': 'chegada', 'tempo': chega}
        elif passa != -1 and (chega == -1 or passa < chega) and (sai == -1 or passa < sai):
            if chega != -1:
                heapq.heappush(self.chegada, chega)
            if sai != -1:
                heapq.heappush(self.saida, sai)
            return {'tipo': 'passagem', 'tempo': passa}
        elif sai != -1:
            if chega != -1:
                heapq.heappush(self.chegada, chega)
            if passa != -1:
                heapq.heappush(self.passagem, passa)
            return {'tipo': 'saida', 'tempo': sai}
        
        return None

    def agenda(self, processo):
        if processo['tipo'] == 'chegada':
            heapq.heappush(self.chegada, processo['tempo'])
        elif processo['tipo'] == 'passagem':
            heapq.heappush(self.passagem, processo['tempo'])
        else:
            heapq.heappush(self.saida, processo['tempo'])