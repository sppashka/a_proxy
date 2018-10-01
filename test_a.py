# coding: utf-8

"""
Test jumping drom proxy to proxy.
"""

from a_proxy import Synchronizer
#import pytest

#@pytest.fixture()
def test_my_add():
    """Unit Test of list"""
    S = Synchronizer()
    S.my_add(1111, ('192.168.0.1', 2222))
    assert S.forwarders[1111] == ('192.168.0.1', 2222)




#while True:
#S.my_run()
#S.my_add(1111, ('192.168.0.1', 2222))

test_my_add()

#ForwarderServer(('192.168.0.171', 433), 433)
