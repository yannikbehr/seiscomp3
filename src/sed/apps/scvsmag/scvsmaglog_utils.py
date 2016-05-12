#!/usr/bin/env python
"""
Convert SeisComP3 Objects into XML strings.

Created on May 9, 2016

@author: behry
"""

import cStringIO
import os

import lxml.etree as ET
import seiscomp3
from seiscomp3.IO import Exporter, ExportSink

class Sink(ExportSink):
    def __init__(self, buf):
        ExportSink.__init__(self)
        self.buf = buf
        self.written = 0

    def write(self, data, size):
        self.buf.write(data[:size])
        self.written += size
        return size


class MessageEncoder:

    def __init__(self, format='qml1.2-rt'):
        ei = seiscomp3.System.Environment.Instance()
        self.transform = None
        if format == 'qml1.2-rt':
            xslt = ET.parse(os.path.join(ei.shareDir(), 'scvsmaglog',
                                         'sc3ml_0.7__quakeml_1.2-RT_eewd.xsl'))
            self.transform = ET.XSLT(xslt)
        elif format == 'shakealert':
            xslt = ET.parse(os.path.join(ei.shareDir(), 'scvsmaglog',
                            'sc3ml_0.7__shakealert.xsl'))
            self.transform = ET.XSLT(xslt)
        elif format == 'sc3ml':
            pass
        else:
            seiscomp3.Logging.error('Currently supported AMQ message formats \
            are sc3ml, qml1.2-rt, and shakealert.')

    def encode(self, ep, pretty_print=True):
        exp = Exporter.Create('trunk')
        io = cStringIO.StringIO()
        sink = Sink(io)
        exp.write(sink, ep)
        # apply XSLT
        dom = ET.fromstring(io.getvalue())
        if self.transform is not None:
            dom = self.transform(dom)
        return ET.tostring(dom, pretty_print=pretty_print)
