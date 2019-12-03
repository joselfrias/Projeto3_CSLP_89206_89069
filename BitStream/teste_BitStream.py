from BitStream import BitReader, BitWriter
import os
import sys
def main():
    with open('test_bitStream.dat', 'wb') as outfile:
        with BitWriter(outfile) as writer:
            chars = '10101010'
            for ch in chars:
                writer.writebits(ord(ch), 1)

    with open('test_bitStream.dat', 'rb') as infile:
        with BitReader(infile) as reader:
            chars = []
            while True:
                x = reader.readbits(8)
                if not reader.read:
                    break
                chars.append(chr(x))
            print(''.join(chars))



main()
