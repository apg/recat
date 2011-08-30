#!/usr/bin/env python
"""This script spits out a log in a simulated real-time based on
information provided at the command line.
"""

import datetime
import optparse
import re
import time
import sys

__author__ = "Andrew Gwozdziewycz <web@apgwoz.com>"
__license__ = "GPLv3"
__version__ = "0.1"

def run_through_lines(f, options):
    last_time = None
    last = f.readline()
    while last:
        next = f.readline()
        ntime = None
        if next:
            ntime = _parse_time(next, options.fields, 
                                options.separator,
                                options.format)
            if ntime == -1:
                sys.stdout.write(next)
                continue
            elif ntime is None:
                sys.exit(1)

            # seed
            if last_time == None:
                last_time = ntime

            diff = abs(ntime - last_time)
#            print "sleeping %f" % (diff / float(options.factor))
            time.sleep(diff / float(options.factor))
            sys.stdout.write(next)
        last = next
        last_time = ntime


def _parse_time(line, fields, separators, format):
    try:
        if re.match('^\s+', line):
            return -1
        else:
            bits = [x for i, x in \
                        enumerate(re.split(separators, line)) 
                    if i % 2 == 0]
            fs = [bits[i-1] for i in fields]
            return time.mktime(datetime.datetime\
                                   .strptime(' '.join(fs), format)\
                                   .timetuple())
    except Exception, e:
        sys.stderr.write("\ncouldn't parse fields into time given format: '%s'" % line)
        return -1


def _parse_separators(sep):
    return '(%s)' % '|'.join(re.escape(s) for s in list(sep))


def _parse_fields(fields):
    try:
        return map(int, fields.split(','))
    except ValueError:
        sys.stderr.write("couldn't parse fields into list of ints")
    return None


def main():
    (options, args) = parser.parse_args()
    parsed_fields = _parse_fields(options.fields)
    if not parsed_fields:
        parser.usage()
        sys.exit(1)
    options.fields = parsed_fields

    parsed_separators = _parse_separators(options.separator)
    if not parsed_separators:
        parser.usage()
        sys.exit(1)
    options.separator = parsed_separators

    if args:
        run_through_lines(open(args[0]), options)
    else:
        run_through_lines(sys.stdin, options)
    sys.exit(0)

usage = "%prog [options] file"
parser = optparse.OptionParser(usage=usage)

parser.add_option("-f", "--fields", help="comma separated list of fields" \
                      " to use for time", 
                  dest="fields", default="1", metavar="FIELDS")
parser.add_option("-n", "--factor", help="speed up factor",
                  dest="factor", type="int", default=1)
parser.add_option("-s", "--separator", help="field separator",
                  dest="separator", default=' ')
parser.add_option("-t", "--time-format", help="time format. see python " \
                      "`datetime.strptime()' for format options",
                  dest="format", default='%Y-%m-%d %H:%M:%s')


if __name__ == '__main__':
    main()
