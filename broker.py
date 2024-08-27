import socket
import select
import time

HOST = 'localhost'
PORT = 65439
PORT2 = 65440
PORT3 = 2004
addr = '127.0.0.1'
addr2 = '127.0.0.1'
addr3 = '127.0.0.1'


ACK_TEXT = 'text_received'


def values():
    global ClientMultiSocket
    ClientMultiSocket = socket.socket()
    print('socket3 instantiated')
    ClientMultiSocket.connect((addr3, PORT3))
    print('socket3 listening')


def heartbeat():
    global ClientMultiSocket
    completed = True
    while not completed:
        Input = time.ctime()
        ClientMultiSocket.send(str.encode(Input))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))
        completed = False


def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket instantiated')

    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket2 instantiated')

    """ClientMultiSocket = socket.socket()
    print('socket3 instantiated')"""

    sock2.bind((HOST, PORT2))
    print('socket2 binded')
    sock2.listen()
    print('socket2 listening')

    ClientMultiSocket = socket.socket()
    print('socket3 instantiated')
    ClientMultiSocket.connect((addr3, PORT3))
    print('socket3 listening')

    conn2, addr = sock2.accept()
    print('socket2 accepted, got connection object')

    connectionSuccessful = False
    while not connectionSuccessful:
        try:
            sock.connect((HOST, PORT))
            print('socket connected')
            connectionSuccessful = True

        except:
            pass

    socks = [sock]

    while True:
        completed = False
        while not completed:
            Input = time.ctime()
            ClientMultiSocket.send(str.encode(Input))

            completed = True

        readySocks, _, _ = select.select(socks, [], [], 5)
        for sock in readySocks:
            message = receiveTextViaSocket(sock)
            topic = receiveTextViaSocket(sock)
            print(str(message))
            print(str(topic))
            sendTextViaSocket(message, conn2)
            sendTextViaSocket(topic, conn2)


def receiveTextViaSocket(sock):

    encodedMessage = sock.recv(1024)

    if not encodedMessage:
        print('error: encodedMessage was received as None')
        return None

    message = encodedMessage.decode('utf-8')

    encodedAckText = bytes(ACK_TEXT, 'utf-8')

    sock.sendall(encodedAckText)
    return (message)


def sendTextViaSocket(message, sock):

    encodedMessage = bytes(message, 'utf-8')

    sock.sendall(encodedMessage)

    encodedAckText = sock.recv(1024)
    ackText = encodedAckText.decode('utf-8')

    if ackText == ACK_TEXT:
        print('Consumer acknowledged reception of text')
    else:
        print('error: server has sent back ' + ackText)


if __name__ == '__main__':
    main()
