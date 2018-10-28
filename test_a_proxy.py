# coding: utf-8

"""
Test jumping drom proxy to proxy.
"""
import socket as s
from collections import namedtuple
import pytest
from a_proxy import Synchronizer

Srv = namedtuple('dummy_server', 'host port')
REAL_IP = s.gethostbyname(s.gethostname())

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

def idparametrize(name, values, fixture=False):
    """Auxiliary decorator for parametrize"""
    return pytest.mark.parametrize(name, values, ids=map(repr, values), indirect=fixture)

@pytest.yield_fixture
def socket():
    """Open and close socket"""
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    yield _socket
    _socket.close()


#@pytest.fixture(scope='module')
#def dummy_server():
#    """Prepare object Host then live full time of runing that module"""
#    class Dummy(object): # pylint: disable=too-few-public-methods
#        """Just any port for test"""
#        host_port = 'localhost', 8080
#        uri = 'http://%s:%s/' % host_port
#
#    return Dummy


@pytest.fixture(scope='module')
def dummy_server(request):
    """Prepare object Host then live full time of runing that module"""
    class Dummy(object): # pylint: disable=too-few-public-methods
        """Just any port for test"""
        def __init__(self, srv):
            self.srv = srv

        @property
        def host_port(self):
            """Just any port for test from parameters"""
            my_str = '{host} {port}'.format(**self.srv._asdict()).split()
            return (my_str[0], int(my_str[1]))


        @property
        def uri(self):
            """Just any port for test from parameters"""
            return 'http://{host}:{port}/'.format(**self.srv._asdict())

    return Dummy(request.param)


@idparametrize('dummy_server', [Srv('localhost', 8080), Srv(REAL_IP, 8080)], fixture=True)
def test_server_connect(socket, dummy_server): # pylint: disable=redefined-outer-name
    """Test open port"""
    socket.connect(dummy_server.host_port)
    assert socket

def test_my_add():
    """Unit Test of list add"""
    test_s = Synchronizer()
    test_s.my_add(1111, ('192.168.0.1', 2222))
    assert test_s.forwarders[1111] == ('192.168.0.1', 2222)

@idparametrize('dummy_server', [Srv('localhost', 1111), Srv(REAL_IP, 1111)], fixture=True)
def test_my_forward(socket, dummy_server): # pylint: disable=redefined-outer-name
    """Test open port 1111"""
    test_s = Synchronizer()
    test_s.go_forward = False
    test_s.my_forward(1111, ('127.0.0.1', 4444))
    socket.connect(dummy_server.host_port)
    assert socket
    test_s.my_remove(1111)

def test_my_remove():
    """Unit Test of list remove"""
    test_s = Synchronizer()
    test_s.my_add(3333, ('127.0.0.1', 2222))
    test_s.my_forward(3333, ('127.0.0.1', 2222))
    test_s.my_remove(3333)
    assert 3333 not in test_s.forwarders
