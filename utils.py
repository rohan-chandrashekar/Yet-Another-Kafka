import logging

ACK_TEXT = 'text_received'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def send_text_via_socket(message, sock):
    try:
        encoded_message = bytes(message, 'utf-8')
        sock.sendall(encoded_message)
        encoded_ack_text = sock.recv(1024)
        ack_text = encoded_ack_text.decode('utf-8')
        if ack_text == ACK_TEXT:
            logging.info('Acknowledged reception of text')
            return True
        else:
            logging.error(f'Unexpected ack: {ack_text}')
            return False
    except Exception as e:
        logging.error(f'Error sending text: {e}')
        return False

def receive_text_via_socket(sock):
    try:
        encoded_message = sock.recv(1024)
        if not encoded_message:
            logging.error('Received None message')
            return None
        message = encoded_message.decode('utf-8')
        sock.sendall(bytes(ACK_TEXT, 'utf-8'))
        return message
    except Exception as e:
        logging.error(f'Error receiving text: {e}')
        return None 