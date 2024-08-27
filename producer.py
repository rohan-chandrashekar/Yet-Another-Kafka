

import socket
import select
import time

HOST = 'localhost'
addr = '127.0.0.1'
PORT = 65439

ACK_TEXT = 'text_received'


def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket instantiated')

    sock.bind((HOST, PORT))
    print('socket binded')

    sock.listen()
    print('socket now listening')

    conn, addr = sock.accept()
    print('socket accepted, got connection object')

    lis = []

    while (True):
        m = int(input("Enter the number of producers to be created: "))
        for i in range(m):
            print("for Producer number:", i+1)
            lis.append((i+1))

            message = input("Enter the message to be sent: ")
            topic = input("Enter the topic: ")
            lis.append(message)
            lis.append(topic)

            sendTextViaSocket(str(lis), conn)
            sendTextViaSocket(str(topic), conn)
            lis.clear()
            time.sleep(2)

        sock.close()


def sendTextViaSocket(message, sock):

    encodedMessage = bytes(message, 'utf-8')

    sock.sendall(encodedMessage)

    encodedAckText = sock.recv(1024)
    ackText = encodedAckText.decode('utf-8')

    if ackText == ACK_TEXT:
        print('Broker acknowledged reception of text')
    else:
        print('error: server has sent back ' + ackText)


if __name__ == '__main__':
    main()
