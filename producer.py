import socket
import time
import argparse
import logging
from utils import send_text_via_socket

HOST = 'localhost'
PORT = 65439

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def main():
    parser = argparse.ArgumentParser(description='Producer for Yet Another Kafka')
    parser.add_argument('--topic', type=str, help='Topic to send messages to')
    parser.add_argument('--message', type=str, help='Message to send')
    parser.add_argument('--count', type=int, default=1, help='Number of producers to simulate')
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((HOST, PORT))
        logging.info('Socket binded')
        sock.listen()
        logging.info('Socket now listening')
        conn, addr = sock.accept()
        logging.info(f'Socket accepted, got connection object from {addr}')

        for i in range(args.count):
            logging.info(f'For Producer number: {i+1}')
            message = args.message or input('Enter the message to be sent: ')
            topic = args.topic or input('Enter the topic: ')
            payload = str([i+1, message, topic])
            send_text_via_socket(payload, conn)
            send_text_via_socket(topic, conn)
            time.sleep(2)
    except Exception as e:
        logging.error(f'Producer error: {e}')
    finally:
        sock.close()

if __name__ == '__main__':
    main()
