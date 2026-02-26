import socket, threading, time
from protocol import enviar_pela_rede_ruidosa
from util.logs import Log
from util.constantes import *
from modulos.enlace import CamadaEnlace
from modulos.rede import CamadaRede
from modulos.transporte import CamadaTransporte

class Cliente:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP_LOCAL, PORTA_CLIENTE))
        self.enlace = CamadaEnlace(MAC_CLIENTE)
        self.rede = CamadaRede(VIP_CLIENTE)
        self.transp = CamadaTransporte()
        self.ack_evento = threading.Event()

    def enviar(self, mensagem):
        # Camada de Aplicação Json
        app_data = {"type": "chat", "sender": VIP_CLIENTE, "message": mensagem, "timestamp": time.time()}
        
        # Encapsulamento em cascata 
        seg = self.transp.criar_segmento(app_data)
        pac = self.rede.criar_pacote(VIP_SERVIDOR, seg)
        quadro_final = self.enlace.preparar_quadro(pac, MAC_ROTEADOR)

        while True:
            Log.info("APLICAÇÃO", f"Enviando Seq {self.transp.seq_atual}: {mensagem}")
            enviar_pela_rede_ruidosa(self.sock, quadro_final, (IP_LOCAL, PORTA_ROTEADOR))
            
            if self.ack_evento.wait(timeout=2.5):
                Log.info("TRANSPORTE", "ACK recebido com sucesso!")
                self.transp.alternar_sequencia()
                self.ack_evento.clear()
                break
            else:
                Log.aviso("TRANSPORTE", f"Timeout! Retransmitindo Seq {self.transp.seq_atual}...")

    def escutar_acks(self):
        while True:
            data, _ = self.sock.recvfrom(4096)
            quadro = self.enlace.receber_e_validar(data)
            if quadro:
                seg = quadro['data']['data']
                if seg['is_ack'] and seg['seq_num'] == self.transp.seq_atual:
                    self.ack_evento.set()

if __name__ == "__main__":
    Log.init()
    c = Cliente()
    threading.Thread(target=c.escutar_acks, daemon=True).start()
    while True:
        msg = input("Mensagem: ")
        c.enviar(msg)