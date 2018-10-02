# coding: utf-8

"""
Test jumping drom proxy to proxy.
"""

import pytest
import socket as s
from a_proxy import Synchronizer

#@pytest.fixture
#def socket(request):
#    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
#    def socket_teardown():
#        _socket.close()
#    request.addfinalizer(socket_teardown)
#    return _socket

@pytest.yield_fixture
def socket():
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    yield _socket
    _socket.close()

@pytest.fixture(scope='module')
def Server():
    class Dummy:
        host_port = 'localhost', 8080
        uri = 'http://%s:%s/' % host_port
    return Dummy

#def test_server_connect(socket):
#    socket.connect(('localhost', 8080))
#    assert socket

def test_server_connect(socket, Server):
    socket.connect(Server.host_port)
    assert socket

def test_my_add():
    """Unit Test of list"""
    test_s = Synchronizer()
    test_s.my_add(1111, ('192.168.0.1', 2222))
    assert test_s.forwarders[1111] == ('192.168.0.1', 2222)




#while True:
#S.my_run()
#S.my_add(1111, ('192.168.0.1', 2222))

#test_my_add()
#test_server_connect()

#ForwarderServer(('192.168.0.171', 433), 433)
