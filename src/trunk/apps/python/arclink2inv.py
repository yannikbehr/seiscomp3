#!/usr/bin/env python

############################################################################
#    Copyright (C) by GFZ Potsdam                                          #
#                                                                          #
#    You can redistribute and/or modify this program under the             #
#    terms of the SeisComP Public License.                                 #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    SeisComP Public License for more details.                             #
############################################################################

import seiscomp3.DataModel, seiscomp3.IO
import getopt
import sys


usage = """arclink2inv [options] input=stdin output=stdout

Options:
  -h [ --help ]      Produce help message
  -f [ --formatted ] Enable formatted XML output
"""


def main(argv):
    imp = seiscomp3.IO.Importer.Create("arclink")
    if imp is None:
        print >> sys.stderr, "Arclink import not available"
        return 1

    formatted = False

    # parse command line options
    try:
        opts, args = getopt.getopt(argv[1:], "hf", ["help", "formatted"])
    except getopt.error, msg:
        print >> sys.stderr, msg
        print >> sys.stderr, "for help use --help"
        return 1

    for o, a in opts:
        if o in ["-h", "--help"]:
            print >> sys.stderr, usage
            return 1
        elif o in ["-f", "--formatted"]:
            formatted = True

    argv = args

    if len(argv) > 0:
        o = imp.read(argv[0])
    else:
        o = imp.read("-")

    inv = seiscomp3.DataModel.Inventory.Cast(o)
    if inv is None:
        print >> sys.stderr, "No inventory found"
        return 1

    ar = seiscomp3.IO.XMLArchive()
    if len(argv) > 1:
        res = ar.create(argv[1])
    else:
        res = ar.create("-")

    if not res:
        print >> sys.stderr, "Failed to open output"
        return 1

    ar.setFormattedOutput(formatted)
    ar.writeObject(inv)
    ar.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

