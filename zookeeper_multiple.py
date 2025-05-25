import socket
import os
from _thread import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    logging.error(str(e))
logging.info('Socket is listening..')
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
    with open('logs.txt', 'a') as file1:
        connection.send(str.encode('Server is working:'))
        while True:
            data = connection.recv(2048)
            if not data:
                break
            response = 'Server message: ' + data.decode('utf-8')
            connection.sendall(str.encode(response))
            logging.info(f'Received data: {data}')
            file1.writelines(str(data))
    connection.close()

while True:
    try:
        Client, address = ServerSideSocket.accept()
        logging.info(f'Connected to: {address[0]}:{address[1]}')
        start_new_thread(multi_threaded_client, (Client, ))
        ThreadCount += 1
        logging.info(f'Thread Number: {ThreadCount}')
    except Exception as e:
        logging.error(f'Zookeeper error: {e}')

ServerSideSocket.close()