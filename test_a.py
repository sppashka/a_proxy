# coding: utf-8

"""
Test jumping drom proxy to proxy.
"""

#import pytest
from a_proxy import Synchronizer


#@pytest.fixture()
def test_my_add():
    """Unit Test of list"""
    test_s = Synchronizer()
    test_s.my_add(1111, ('192.168.0.1', 2222))
    assert test_s.forwarders[1111] == ('192.168.0.1', 2222)




#while True:
#S.my_run()
#S.my_add(1111, ('192.168.0.1', 2222))

test_my_add()

#ForwarderServer(('192.168.0.171', 433), 433)
