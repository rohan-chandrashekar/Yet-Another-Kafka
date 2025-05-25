import socket
import time
import argparse
import logging
from utils import send_text_via_socket, receive_text_via_socket

HOST = 'localhost'
PORT = 65440

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def fetch_topics(topics=None, count=1):
    TopicNames = []
    if topics:
        TopicNames = topics
    else:
        n = count
        for i in range(n):
            topic = input('Enter the topic to be subscribed to: ')
            TopicNames.append(topic)
    return TopicNames

def main():
    parser = argparse.ArgumentParser(description='Consumer for Yet Another Kafka')
    parser.add_argument('--topics', nargs='+', help='Topics to subscribe to')
    parser.add_argument('--count', type=int, default=1, help='Number of consumers to simulate')
    parser.add_argument('--from-beginning', action='store_true', help='Read from beginning')
    args = parser.parse_args()

    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock2.connect((HOST, PORT))
        logging.info('Socket2 connected')
        temp_arr = fetch_topics(args.topics, args.count)
        while True:
            message = receive_text_via_socket(sock2)
            topic = receive_text_via_socket(sock2)
            if topic in temp_arr:
                logging.info(f'Message received for topic {topic}: {message}')
    except Exception as e:
        logging.error(f'Consumer error: {e}')
    finally:
        sock2.close()

if __name__ == '__main__':
    main()
