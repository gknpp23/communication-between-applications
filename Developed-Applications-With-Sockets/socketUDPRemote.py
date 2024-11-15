#!/usr/bin/env python3

import argparse, random, socket, sys

MAX_BYTES = 65535

def servidor(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Servidor >> Escutando no IP e porta', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if random.random() < 0.5: # Sorteio aleatório para decidir se essa solicitação será atendida
            print('Servidor >> Fingindo descartar pacote de {}'.format(address))
            continue
        text = data.decode('ascii')
        print('Servidor >> O cliente no IP e porta {} enviou a mensagem {!r}'.format(address, text))
        message = 'Mensagem para o cliente: O dado enviado possui comprimento de {} bytes'.format(len(data))
        sock.sendto(message.encode('ascii'), address)

def cliente(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((hostname, port))
    print('Cliente >> Nome do socket do cliente: {}'.format(sock.getsockname()))

    delay = 0.1  # Tempo de espera inicial em segundos
    text = 'Mensagem para o servidor: Estou enviando uma mensagem'
    data = text.encode('ascii')
    while True:
        sock.send(data)
        print('Cliente >> Aguardando {} segundos para enviar a resposta'.format(delay))
        sock.settimeout(delay) # Define o tempo em que o cliente espera pela resposta do servidor
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout as exc: # Chamada seja interrompida com uma exceção socket.timeout quando uma chamada tiver esperado por muito tempo
            delay *= 2  # Backoff exponencial: Espere ainda mais pelo próximo pedido
            if delay > 2.0: # Desiste depois de ter feito tentativas suficientes
                raise RuntimeError('Cliente >> Eu acho que o servidor caiu') from exc
        else:
            break   # terminamos e podemos parar de repetir

    print('Cliente >> O servidor respondeu {!r}'.format(data.decode('ascii')))

if __name__ == '__main__':
    choices = {'cliente': cliente, 'servidor': servidor}
    parser = argparse.ArgumentParser(description='Enviar e receber UDP, fingindo que os pacotes são frequentemente descartados')
    parser.add_argument('regra', choices=choices, help='Qual regra sera desempenhada.')
    parser.add_argument('host', help='interface o servidor escuta; host o cliente envia')
    parser.add_argument('-p', metavar='PORTA', type=int, default=1060, help='Porta UDP (padrao: 1060)')
    args = parser.parse_args()
    function = choices[args.regra]
    function(args.host, args.p)
    
    
