#!/usr/bin/env python
"""
Interface to the UserDisplay.
Created on May 7, 2013

@author: behry
"""

import cStringIO
import datetime
import os
import time

import lxml.etree as ET
import seiscomp3
from stompy.simple import Client


class UDException(Exception): pass


class UDConnection:

    def __init__(self, host=None, port=None, topic=None, username=None,
                 password=None):
        try:
            self.topic = topic
            self.username = username
            self.password = password
            self.host = host
            self.port = port
            self.stomp = Client(host=self.host, port=self.port)
            self.stomp.connect(username=self.username, password=self.password)
        except Exception, e:
            raise UDException('Cannot connect to message broker (%s@%s:%d): %s.'\
                               % (username, host, port, e))

    def send(self, msg):
        try:
            self.stomp.put(msg, destination=self.topic)
        except Exception, e:
            seiscomp3.Logging.error("ActiveMQ connection lost.")
            # Wait for a bit in case the ActiveMQ broker is restarting
            time.sleep(10)
            try:
                del self.stomp
                self.stomp = Client(host=self.host, port=self.port)
                self.stomp.connect(username=self.username, password=self.password)
            except Exception, e:
                raise UDException('Cannot reconnect to server: %s' % e)
            seiscomp3.Logging.info('Connection re-established.')


class HeartBeat(UDConnection):

    def __init__(self, host, port, topic, username, password,
                 format='qml1.2-rt'):
        UDConnection.__init__(self, host, port, topic, username, password)
        self.format = format

    def send_hb(self):
        dt = datetime.datetime.utcnow()
        root = ET.Element('hb')
        root.set('originator', 'vssc3')
        root.set('sender', 'vssc3')
        if self.format == 'qml1.2-rt':
            now = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            root.set('xmlns', 'http://heartbeat.reakteu.org')
        else:
            now = dt.strftime('%a %B %d %H:%M:%S %Y')
        root.set('timestamp', now)
        tree = ET.ElementTree(root)
        f = cStringIO.StringIO()
        tree.write(f, encoding="UTF-8", xml_declaration=True, method='xml')
        msg = f.getvalue()
        self.send(msg)
        return msg


if __name__ == '__main__':
    pass
