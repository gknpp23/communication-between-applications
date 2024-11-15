#!/usr/bin/env python3

import argparse, socket
from datetime import datetime

MAX_BYTES = 65535

def servidor(porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria um socket simples 
    sock.bind(('127.0.0.1', porta)) # Solicita um endereço de rede UDP
    print('Servidor >> Escutando no IP e porta {}'.format(sock.getsockname()))
    while True: # Executa repetidamente recvfrom()
        data, address = sock.recvfrom(MAX_BYTES) # Recebe mensagens ate 65.535 bytes; retorna o endereço do cliente e conteúdo do datagrama no formato de bytes
        text = data.decode('ascii')
        print('Servidor >> O cliente no IP e porta {} enviou a mensagem {!r}'.format(address, text))
        text = 'Mensagem para o cliente: O dado enviado possui comprimento de {} bytes'.format(len(data))
        data = text.encode('ascii')
        sock.sendto(data, address) # Datagrama de resposta enviado ao cliente

def cliente(porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = 'Mensagem para o servidor: Hora atual {}'.format(datetime.now())
    data = text.encode('ascii')
    sock.sendto(data, ('127.0.0.1', porta)) # Possui uma mensagem e um endereço de destino
    print('Cliente >> O sistema operacional do cliente informou o IP e porta {}'.format(sock.getsockname())) # O SO atribui um IP e porta, na saída da chamada getsockname()
    data, address = sock.recvfrom(MAX_BYTES) #Cliente Prosmicuo
    text = data.decode('ascii')
    print('Cliente >> O servidor {} respondeu {!r}'.format(address, text))

if __name__ == '__main__':
    choices = {'cliente': cliente, 'servidor': servidor}
    parser = argparse.ArgumentParser(description='Enviar e receber UDP localmente')
    parser.add_argument('regra', choices=choices, help='Qual regra sera desempenhada.')
    parser.add_argument('-p', metavar='PORTA', type=int, default=1060, help='Porta UDP (padrao: 1060)')
    args = parser.parse_args()
    function = choices[args.regra]
    function(args.p)
