from protocol import Segmento

class CamadaTransporte:
    def __init__(self):
        self.seq_atual = 0  # Bit 0 ou 1 para stop-and-wait

    def criar_segmento(self, payload_json, is_ack=False):
        return Segmento(self.seq_atual, is_ack, payload_json).to_dict()

    def alternar_sequencia(self):
        self.seq_atual = 1 - self.seq_atual