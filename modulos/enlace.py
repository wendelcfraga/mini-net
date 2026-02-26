from protocol import Quadro
from util.logs import Log

class CamadaEnlace:
    def __init__(self, mac_local):
        self.mac_local = mac_local

    def preparar_quadro(self, pacote_dict, mac_destino):
        # Cria o quadro e calcula o CRC automaticamente na serialização
        quadro = Quadro(self.mac_local, mac_destino, pacote_dict)
        return quadro.serializar()

    def receber_e_validar(self, bytes_crus):
        dados, integro = Quadro.deserializar(bytes_crus)
        if not integro:
            Log.erro("ENLACE", "Erro de CRC detectado! Descartando quadro.") 
            return None
        return dados