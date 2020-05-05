import pytest
import queue
import socket
from .simple_sender import SimpleSender, MESSAGE
from ...connected_player.listener import Listener


QUEUE = queue.Queue()

@pytest.fixture
def listener():
    return Listener(QUEUE)

def test_if_server_accepts_new_client(listener):
    client = SimpleSender(listener.port)
    client.start()
    conn, addr = listener.listen_for_client()
    assert addr[0] == socket.gethostbyname(socket.gethostname()) # Same address (localhost)
    assert type(conn) == socket.socket # Proper socket was connected
    assert conn.family == socket.AddressFamily.AF_INET
    assert conn.type == socket.SocketKind.SOCK_STREAM

def test_if_message_from_client_is_received_properly(listener):
    client = SimpleSender(listener.port)
    client.start()
    listener.listen_for_client()
    listener.start()
    assert QUEUE.get() == MESSAGE
