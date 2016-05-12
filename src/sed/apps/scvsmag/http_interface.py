#!/usr/bin/env python
'''
HTTP interface to forward XML messages to a webserver.

Created on May 9, 2016

@author: behry
'''

import httplib
import struct
import urllib


class HTTPInterface:

    def __init__(self, host, port, script=None):
        self.headers = {"Content-type": "application/xml",
                        "Accept": "text/plain"}
        self.host = host
        self.port = port
        self.url = 'http://%s' % host
        if script is not None:
            self.url += '/%s' % script

    def send(self, msg):
        conn = httplib.HTTPConnection(self.host, self.port)
        params = urllib.urlencode({'qml':msg})
        conn.request("POST", self.url, body=params)
        response = conn.getresponse()
        conn.close()
        return (response.status, response.reason)

def send_msg(sock, msg):
    sock.sendall(msg)
