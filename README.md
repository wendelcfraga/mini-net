
# Projeto Mini-NET

Este projeto consiste na implementação de uma pilha de protocolos de rede customizada sobre **UDP**, seguindo a abordagem **Top-Down** para desmistificar o funcionamento da Internet e das camadas OSI/TCP-IP.

## 🛠️ Tecnologias e Restrições

**Linguagem:** Python 3.8+.

**Bibliotecas:** Apenas bibliotecas padrão (`socket`, `threading`, `json`, `zlib`, etc.).

**Protocolo Base:** UDP (`SOCK_DGRAM`) para todas as fases de confiabilidade.

**Proibições:** Não é permitido o uso de frameworks de alto nível (Flask, Scapy) ou TCP após a Fase 1.


## 📂 Estrutura do Projeto

A arquitetura foi dividida em módulos independentes para garantir o encapsulamento estrito (a Camada N só conversa com a N-1):

```text
Projeto_MiniNet/
├── protocolo.py           # Biblioteca base e simulador de canal ruidoso.
├── client.py              # Interface do usuário e lógica de envio.
├── server.py              # Receptor final e lógica de ACKs.
├── router.py              # Roteador intermediário (Fase 3).
├── util/
│   ├── logs.py            # Classe auxiliar para logs coloridos (ANSI).
│   └── constantes.py      # Definição de VIPs, MACs e Portas.
└── modulos/
    ├── transporte.py      # Camada 4: Stop-and-Wait, ACKs e Timeouts.
    ├── rede.py            # Camada 3: Endereçamento lógico (VIP) e TTL.
    └── enlace.py          # Camada 2: Endereçamento físico (MAC) e CRC32.

```

## 🚀 Como Executar

Para uma demonstração completa, abra **três terminais** e execute os comandos na seguinte ordem:

1. **Terminal 1 (Roteador):**
```bash
python router.py

```


2. **Terminal 2 (Servidor):**
```bash
python server.py

```


3. **Terminal 3 (Cliente):**
```bash
python client.py

```



## 🛡️ Funcionalidades Implementadas

### 1. Confiabilidade (Fase 2)

Implementação do protocolo **Stop-and-Wait**. O cliente aguarda um **ACK** (confirmação) antes de enviar o próximo bit de sequência (0 ou 1). Caso ocorra perda, o **Timeout** dispara a retransmissão automática.

### 2. Roteamento (Fase 3)

O cliente envia dados para endereços virtuais (ex: `SERVIDOR_PRIME`). O script `router.py` consulta uma tabela estática, decrementa o **TTL** (Time to Live) e encaminha para o destino correto.

### 3. Integridade (Fase 4)

Uso de **Checksum/CRC32** para detecção de corrupção de bits. Se a camada física (`protocolo.py`) corromper o dado, o receptor detecta o erro via CRC e descarta o quadro silenciosamente, forçando a camada de transporte a recuperar a perda por timeout.

## 📊 Diagnóstico por Logs

O sistema utiliza logs coloridos para facilitar o debug conforme as "Dicas para o Sucesso":

* 🟢 **VERDE:** Camada de Aplicação (Mensagens enviadas/recebidas).
* 🟡 **AMARELO:** Camada de Transporte (Retransmissões e ACKs).
* 🔵 **AZUL:** Camada de Rede (Roteamento e TTL).
* 🔴 **VERMELHO:** Camada de Enlace/Física (Erros de CRC e descartes).

## 🎓 Avaliação

Este código foi projetado para atender aos critérios de resiliência (teste com 50% de perda).

---

**Desenvolvido para a disciplina de Redes de Computadores - 2025/4.** 

---
## 🎥 Demonstração em Vídeo

Para visualizar o projeto em funcionamento, incluindo os testes de resiliência e a análise dos logs das camadas, acesse o link abaixo:

[![Assista ao Vídeo](https://img.shields.io/badge/YouTube-Assistir%20Vídeo-red?style=for-the-badge&logo=youtube)](https://drive.google.com/file/d/1lQPO1VQwbDibQ28vUH0DJiGCTr2pFBqN/view?usp=drive_link)
