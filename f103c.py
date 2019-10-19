#!/bin/python
import argparse
import collections
import serial
import re

Sample = collections.namedtuple('Sample', 'channel raw voltage'.split())


def fix_types(groups):
    groups['channel'] = int(groups['channel'])
    groups['voltage'] = float(groups['voltage'])
    groups['raw'] = int(groups['raw'])
    return groups


def readvals(ser):
    while True:
        line = ser.read_until()
        line = line.decode('ascii').strip()
        if line:
            pattern = r'CH(?P<channel>.):(?P<raw>\d+)\t(?P<voltage>[.\d]+)V'
            m = re.match(pattern, line)
            yield Sample(**fix_types(m.groupdict()))


def main():
    parser = argparse.ArgumentParser(description='Read voltages from f103c')
    parser.add_argument('--channel', type=int,
                        help='the channel to output')
    parser.add_argument('--device', default='/dev/ttyUSB0', type=str,
                        help='the path to the f103c device serial interface')
    args = parser.parse_args()
    with serial.Serial(args.device, 115200, timeout=2) as ser:
        for sample in readvals(ser):
            if args.channel:
                 if sample.channel == args.channel:
                     print(sample.voltage)
            else:
                print(sample)


if __name__ == "__main__":
    main()
