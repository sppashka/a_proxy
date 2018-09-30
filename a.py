#/usr/bin/env python
# -*- coding: cp1251 -*-

"""
Jumping drom proxy to proxy.
"""

import sys
import select
import socket

from threading import Thread

####

from time import sleep
from urllib2 import urlopen, HTTPError, URLError

try:
    import cPickle as pickle
except ImportError:
    import pickle

DICTURL = 'http://127.0.0.1/114.txt'

####

class ConnectionLost(Exception):
    """That class don't do nothing."""
    try:
        raise 'str'
    except TypeError:
        pass
    else:
        assert False

####

def forward(client_sock, server_sock, timeout):
    """Connected our port with proxy."""
    slist = [client_sock, server_sock]

    while True:
        readables, writeables, exceptions = select.select(slist, slist, [], timeout)
        if (exceptions or (readables, writeables, exceptions) == ([], [], [])):
            raise ConnectionLost
        data = ''
        for readable_sock in readables:
            writeableslist = [client_sock, server_sock]
            writeableslist.remove(readable_sock)
            data = readable_sock.recv(512)

            #print ">>>  RECV : %s" % data

            if data:
                print ">>>  RECV : %s" % data
                writeableslist[0].send(data)
            else:
                raise ConnectionLost
        data1 = ''
        for writeable_sock in writeables:
            readableslist = [client_sock, server_sock]
            readableslist.remove(writeable_sock)
            data1 = writeable_sock.recv(512)
            print ">>>  TR : %s" % data1
            if data1:
                print ">>>  TR : %s" % data1
                readableslist[0].send(data1)
            else:
                raise ConnectionLost

####

class ForwarderClient(Thread):
    """Client connect to our port."""

    def __init__(self, (from_sock, from_addr), to_addr):
        Thread.__init__(self)
        self.from_sock = from_sock
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.to_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.to_sock.connect(to_addr)
        self.timeout = 50
        self.start()

    def run(self):
        try:
            self.to_sock.connect(self.to_addr)
            forward(self.from_sock, self.to_sock, self.timeout)

        except socket.error, msg:
            print '%s' % msg

        else:
            pass

        self.to_sock.close()
        self.from_sock.close()

####

class ForwarderServer(Thread):
    """Server open or listen our port."""

    def __init__(self, addr, port):
        Thread.__init__(self)
        self.port = port
        self.addr = addr
        self.go_forward = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", port))
        self.sock.listen(1)
        self.start()

    def run(self):
        print '+ crtating server at %d, %s' % (self.port, repr(self.addr))
        while self.go_forward:
            ForwarderClient(self.sock.accept(), self.addr)

    def remove(self):
        """Forget that proxy."""
        print '+ removing server at %s' % self.port
        self.go_forward = False
        self.sock.close()

####

class Synchronizer(Thread):
    """Open file with proxy and remember in dict what the proxy
        we have use and orget what the proxy not on the file (correct memory)."""

    def __init__(self):
        Thread.__init__(self)
        self.forwarders = {}
        self.pickled_dict = {}
        #self.start()

    def my_switch(self):
        """Swithc operation"""
        unpickled_dict = pickle.loads(self.pickled_dict)

        for port, addr in unpickled_dict.items():
            if port in self.forwarders:
                if self.forwarders[port].addr != addr:
                    print 'changing forwarder addr on %d to %s' % (port, addr)
                    self.forwarders[port].addr = addr

                else:
                    self.forwarders[port] = ForwarderServer(addr, port)

        for port in self.forwarders.iterkeys():
            if port not in unpickled_dict:
                self.forwarders[port].remove()
                del self.forwarders[port]


    def my_run(self):
        """FSM by parsing state of dict in two lists."""
        try:
            self.pickled_dict = urlopen(DICTURL).read()

        except HTTPError as error:
            print '>> The server couldn\'t fulfill the request.'
            print '>> Error code: ', error.code

        except URLError as error:
            print '>> We failed to reach a server.'
            print '>> Reason: ', error.reason
            print '>>', sys.exc_info()[1]

        else:
            self.my_switch()
        finally:
            sleep(10)

####

S = Synchronizer()

while True:
    S.my_run()

ForwarderServer(('192.168.0.171', 433), 433)
