import os
import sys

class Log:
    VERMELHO = "\033[91m"  # Erros físicos/CRC
    VERDE = "\033[92m"     # Aplicação
    AMARELO = "\033[93m"   # Transporte/Retransmissão
    AZUL = "\033[94m"      # Rede/Roteamento
    RESET = "\033[0m"

    @staticmethod
    def init():
        # Habilita o suporte a cores no CMD do Windows
        if sys.platform == "win32":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    @staticmethod
    def info(camada, msg):
        print(f"{Log.VERDE}[{camada.upper()}] {msg}{Log.RESET}")

    @staticmethod
    def aviso(camada, msg):
        print(f"{Log.AMARELO}[{camada.upper()}] {msg}{Log.RESET}")

    @staticmethod
    def erro(camada, msg):
        print(f"{Log.VERMELHO}[{camada.upper()}] {msg}{Log.RESET}")

    @staticmethod
    def rede(camada, msg):
        print(f"{Log.AZUL}[{camada.upper()}] {msg}{Log.RESET}")