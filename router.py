import socket
from util.logs import Log
from util.constantes import *
from modulos.enlace import CamadaEnlace
from protocol import enviar_pela_rede_ruidosa

# Tabela de Roteamento Estática da fase 3: req 4
# VIP -> (IP Real, Porta Real)

TABELA_ROTAS = {
    VIP_SERVIDOR: (IP_LOCAL, PORTA_SERVIDOR),
    VIP_CLIENTE: (IP_LOCAL, PORTA_CLIENTE)
}

class Roteador:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP_LOCAL, PORTA_ROTEADOR))
        self.enlace = CamadaEnlace(MAC_ROTEADOR)

    def iniciar(self):
        Log.rede("ROTEADOR", f"Operando na porta {PORTA_ROTEADOR}...")
        
        while True:
            data, _ = self.sock.recvfrom(4096)
            
            # O roteador também verifica integridade do quadro da camada 2
            quadro = self.enlace.receber_e_validar(data)
            if not quadro:
                continue

            pacote = quadro['data']
            destino_vip = pacote['dst_vip']
            
            pacote['ttl'] -= 1
            if pacote['ttl'] <= 0:
                Log.erro("ROTEADOR", f"Pacote para {destino_vip} descartado (TTL=0)")
                continue

            if destino_vip in TABELA_ROTAS:
                endereco_real = TABELA_ROTAS[destino_vip]
                Log.rede("ROTEADOR", f"Encaminhando pacote para {destino_vip} em {endereco_real}")
                
                enviar_pela_rede_ruidosa(self.sock, data, endereco_real)
            else:
                Log.erro("ROTEADOR", f"Destino {destino_vip} não encontrado na tabela de rotas.")

if __name__ == "__main__":
    Log.init()
    Roteador().iniciar()