from protocol import Pacote

class CamadaRede:
    def __init__(self, vip_local):
        self.vip_local = vip_local

    def criar_pacote(self, vip_destino, segmento_dict):
        # Encapsula o segmento em um pacote com TTL inicial
        return Pacote(self.vip_local, vip_destino, ttl=10, segmento_dict=segmento_dict).to_dict()

    def validar_ttl(self, pacote_dict):
        if pacote_dict['ttl'] <= 0:
            return False
        return True