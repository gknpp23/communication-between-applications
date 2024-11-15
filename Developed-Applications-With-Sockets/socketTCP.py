#!/usr/bin/env python3
# Cliente e servidor TCP simples que enviam e recebem 16 octetos

import argparse, socket

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('esperava %d bytes, mas recebeu apenas %d bytes antes do fechamento do socket' % (length, len(data)))
        data += more
    return data

def servidor(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # SO_REUSEADDR permite que um socket seja vinculado à força a uma porta em uso por outro socket
    sock.bind((interface, port)) # Reivindica uma porta especifica
    sock.listen(1) # O programa decide virar um servidor 
    print('Escutando em', sock.getsockname())
    while True:
        print('Esperando para aceitar uma nova conexao')
        sc, sockname = sock.accept() # Aguarda pedidos de conexões
        print('Aceito uma conexao de ', sockname)
        print('  Nome do socket:', sc.getsockname()) # Visualizar qual porta TCP o socket está usando no local
        print('  Par do socket:', sc.getpeername()) # Visualizar o endereço do cliente ao qual um soquete conectado está vinculado
        message = recvall(sc, 16)
        print('  Recebendo mensagem do tipo 16 octetos:', repr(message))
        sc.sendall(b'Fechado, cliente') # Envia os dados. Obs.: Atencao ao conteudo
        sc.close()
        print('  Resposta enviada, socket fechado')

def cliente(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port)) # Inicia o three-way handshake entre o cliente e o servidor
    print('O cliente recebeu um nome de socket', sock.getsockname())
    sock.sendall(b'Enviei, servidor') # Envia os dados. Obs.: Atencao ao conteudo
    reply = recvall(sock, 16)
    print('O servidor diz', repr(reply))
    sock.close()

if __name__ == '__main__':
    choices = {'cliente': cliente, 'servidor': servidor}
    parser = argparse.ArgumentParser(description='Enviar e receber usando TCP')
    parser.add_argument('regra', choices=choices, help='Qual regra sera desempenhada.')
    parser.add_argument('host', help='interface o servidor escuta; host o cliente envia')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='Porta TCP (padrao: 1060)')
    args = parser.parse_args()
    function = choices[args.regra]
    function(args.host, args.p)
