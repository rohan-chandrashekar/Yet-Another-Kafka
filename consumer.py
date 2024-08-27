

import socket
import select
import time

HOST = 'localhost'
PORT = 65440
addr = '127.0.0.1'

ACK_TEXT = 'text_received'


def fetch_topics():
    TopicNames = []

    n = int(input("Enter the number of consumers to be created: "))
    for i in range(n):
        print("for each consumer, enter the topic to be subscribed to: ")
        topic = input("Enter the topic: ")

        TopicNames.append(topic)

    return TopicNames


def main():

    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket2 instantiated')

    connectionSuccessful = False
    while not connectionSuccessful:
        try:
            sock2.connect((HOST, PORT))
            print('socket2 connected')
            connectionSuccessful = True
        except:
            pass

    temp_arr = fetch_topics()

    socks = [sock2]
    while True:

        readySocks, _, _ = select.select(socks, [], [], 5)

        for sock2 in readySocks:
            message = receiveTextViaSocket(sock2)
            topic = receiveTextViaSocket(sock2)

            stuff = []
            if topic in temp_arr:
                for i in range(len(temp_arr)):
                    if (temp_arr[i] == topic):
                        stuff.append(i+1)

                print("To Consumer Numbers: ")
                print(stuff)
                print("Message received from producer Number: " + message[1])
                print("Message and Topic Recieved: [" + message[3:])
                stuff.clear()


def sendTextViaSocket(message, sock):

    encodedMessage = bytes(message, 'utf-8')

    sock.sendall(encodedMessage)

    encodedAckText = sock.recv(1024)
    ackText = encodedAckText.decode('utf-8')

    if ackText == ACK_TEXT:
        print('Broker acknowledged reception of text')
    else:
        print('error: server has sent back ' + ackText)


def receiveTextViaSocket(sock):

    encodedMessage = sock.recv(1024)

    if not encodedMessage:
        print('error: encodedMessage was received as None')
        return None

    message = encodedMessage.decode('utf-8')

    encodedAckText = bytes(ACK_TEXT, 'utf-8')

    sock.sendall(encodedAckText)

    return message


if __name__ == '__main__':
    main()
