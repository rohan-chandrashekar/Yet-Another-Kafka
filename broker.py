import socket
import select
import time
import logging
from utils import send_text_via_socket, receive_text_via_socket

HOST = 'localhost'
PORT = 65439
PORT2 = 65440
PORT3 = 2004

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock2.bind((HOST, PORT2))
        logging.info('Socket2 binded')
        sock2.listen()
        logging.info('Socket2 listening')
        client_multi_socket = socket.socket()
        client_multi_socket.connect(('127.0.0.1', PORT3))
        logging.info('Socket3 connected to Zookeeper')
        conn2, addr = sock2.accept()
        logging.info(f'Socket2 accepted, got connection object from {addr}')
        connection_successful = False
        while not connection_successful:
            try:
                sock.connect((HOST, PORT))
                logging.info('Socket connected')
                connection_successful = True
            except Exception:
                time.sleep(1)
        socks = [sock]
        while True:
            client_multi_socket.send(str.encode(time.ctime()))
            ready_socks, _, _ = select.select(socks, [], [], 5)
            for ready_sock in ready_socks:
                message = receive_text_via_socket(ready_sock)
                topic = receive_text_via_socket(ready_sock)
                logging.info(f'Received message: {message}, topic: {topic}')
                send_text_via_socket(message, conn2)
                send_text_via_socket(topic, conn2)
    except Exception as e:
        logging.error(f'Broker error: {e}')
    finally:
        sock.close()
        sock2.close()

if __name__ == '__main__':
    main()
