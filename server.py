import socket
from protocol import enviar_pela_rede_ruidosa
from util.logs import Log
from util.constantes import *
from modulos.enlace import CamadaEnlace
from modulos.rede import CamadaRede
from modulos.transporte import CamadaTransporte

class Servidor:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP_LOCAL, PORTA_SERVIDOR))
        
        self.enlace = CamadaEnlace(MAC_SERVIDOR)
        self.rede = CamadaRede(VIP_SERVIDOR)
        self.transp = CamadaTransporte()
        
        self.ultimo_seq_recebido = -1 # Detectar duplicatas (Fase 2)

    def rodar(self):
        Log.info("SISTEMA", f"Servidor Mini-NET aguardando em {IP_LOCAL}:{PORTA_SERVIDOR}")
        
        while True:
            dados_brutos, addr_origem = self.sock.recvfrom(4096)
            
            # --- camada de enlace ---
            quadro = self.enlace.receber_e_validar(dados_brutos)
            if not quadro:
                # O log de erro de CRC já é disparado dentro do módulo enlace
                continue

            # --- camada de rede ---
            pacote = quadro['data']
            if not self.rede.validar_ttl(pacote):
                Log.rede("REDE", "TTL expirado. Descartando pacote.")
                continue
            
            # --- camada de transporte ---
            segmento = pacote['data']
            seq_recebido = segmento['seq_num']
            
            if seq_recebido != self.ultimo_seq_recebido:
                # --- camada de aplicação ---
                msg_app = segmento['payload']
                Log.info("APLICAÇÃO", f"[{msg_app['sender']}]: {msg_app['message']}")
                self.ultimo_seq_recebido = seq_recebido
            else:
                Log.aviso("TRANSPORTE", f"Duplicata Seq {seq_recebido} detectada. Reenviando ACK.")

            self.enviar_confirmacao(seq_recebido, pacote['src_vip'], quadro['src_mac'], addr_origem)

    def enviar_confirmacao(self, seq_num, vip_destino, mac_destino, addr_real):
        
        seg_ack = self.transp.criar_segmento(payload_json=None, is_ack=True)
        seg_ack['seq_num'] = seq_num 
        
        pac_ack = self.rede.criar_pacote(vip_destino, seg_ack)
        quadro_ack = self.enlace.preparar_quadro(pac_ack, mac_destino)
        
        Log.aviso("TRANSPORTE", f"Enviando ACK {seq_num}")
        enviar_pela_rede_ruidosa(self.sock, quadro_ack, addr_real)

if __name__ == "__main__":
    Log.init()
    Servidor().rodar()