# coding: utf-8

"""
Test jumping drom proxy to proxy.
"""
import socket as s
import pytest
from a_proxy import Synchronizer

#@pytest.fixture
#def socket(request):
#    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
#    def socket_teardown():
#        _socket.close()
#    request.addfinalizer(socket_teardown)
#    return _socket

#def test_server_connect(socket):
#    socket.connect(('localhost', 8080))
#    assert socket

@pytest.yield_fixture
def socket():
    """Open and close socket"""
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    yield _socket
    _socket.close()

@pytest.fixture(scope='module')
def dummy_server():
    """Prepare object Host then live full time of runing that module"""
    class Dummy(object): # pylint: disable=too-few-public-methods
        """Just any port for test"""
        host_port = 'localhost', 8080
        uri = 'http://%s:%s/' % host_port

    return Dummy


def test_server_connect(socket, dummy_server): # pylint: disable=redefined-outer-name
    """Test open port"""
    socket.connect(dummy_server.host_port)
    assert socket

def test_my_add():
    """Unit Test of list add"""
    test_s = Synchronizer()
    test_s.my_add(1111, ('192.168.0.1', 2222))
    assert test_s.forwarders[1111] == ('192.168.0.1', 2222)

def test_my_remove():
    """Unit Test of list remove"""
    test_s = Synchronizer()
    test_s.my_add(1111, ('192.168.0.1', 2222))
    test_s.my_forward(1111, ('192.168.0.1', 2222))
    test_s.my_remove(1111)
    assert (1111 not in test_s.forwarders)
