import unittest
from unittest.mock import Mock
from utils import send_text_via_socket, receive_text_via_socket, ACK_TEXT

class TestUtils(unittest.TestCase):
    def test_send_text_via_socket_ack(self):
        mock_sock = Mock()
        mock_sock.recv.return_value = ACK_TEXT.encode('utf-8')
        result = send_text_via_socket('hello', mock_sock)
        self.assertTrue(result)
        mock_sock.sendall.assert_called()

    def test_send_text_via_socket_unexpected_ack(self):
        mock_sock = Mock()
        mock_sock.recv.return_value = b'wrong_ack'
        result = send_text_via_socket('hello', mock_sock)
        self.assertFalse(result)

    def test_receive_text_via_socket_success(self):
        mock_sock = Mock()
        mock_sock.recv.return_value = b'world'
        result = receive_text_via_socket(mock_sock)
        self.assertEqual(result, 'world')
        mock_sock.sendall.assert_called_with(ACK_TEXT.encode('utf-8'))

    def test_receive_text_via_socket_none(self):
        mock_sock = Mock()
        mock_sock.recv.return_value = b''
        result = receive_text_via_socket(mock_sock)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main() 