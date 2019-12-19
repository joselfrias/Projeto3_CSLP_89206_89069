import time
class Stream(object):

    def __init__(self):
        self.accumulator = 0
        self.bcount = 0
        self.y = []
        self.u = []
        self.v = []
        self.matrix = ''

    def writeBit(self, bit):
        if self.bcount == 8:
            if self.matrix == 'y':
                self.y.append(self.accumulator)
            elif self.matrix == 'u':
                self.u.append(self.accumulator)
            elif self.matrix == 'v':
                self.v.append(self.accumulator)
            self.accumulator = 0
            self.bcount = 0
        if bit > 0:
            self.accumulator |= 1 << 7-self.bcount
        self.bcount +=1

    def writeBits(self, bits, n):
        while n > 0:
            self.writeBit(bits & 1 << n-1)
            n -= 1

    def writeAll(self , outFile):
        file = open(outFile, 'wb')
        for data in self.y:
            print(data)
            time.sleep(1)
            file.write(bytearray([data]))
        for data in self.u:
            file.write(bytearray([data]))
        for data in self.v:
            file.write(bytearray([data]))
        self.y = []
        self.u = []
        self.v = []
        if self.accumulator != 0:
            file.write(bytearray([self.accumulator]))
        file.close()

    def readbit(self, file):
        if not self.bcount:
            a = file.read(1)
            if a:
                self.accumulator = ord(a)
            self.bcount = 8
            self.read = len(a)
        rv = (self.accumulator & (1 << self.bcount-1)) >> self.bcount-1
        self.bcount -= 1
        return rv

    def resetAll(self):
        self.accumulator = 0
        self.bcount = 0

    def readbits(self, n, nFile):
        file = nFile
        v = 0
        while n > 0:
            v = (v << 1) | self.readbit(file)
            n -= 1
        return v

    def setMatrix(self, matrix):
        self.matrix = matrix

'''
def main():
        inpu = '11111111' #[1, 1, 1, 1, 1, 1, 1, 1,  1, 1, 1, 1, 1, 1, 1, 1,  1, 0, 0, 0, 0, 0, 0]
        stream = Stream()
        stream.setMatrix('y')
        stream.writeBits(int(inpu,2), 8)
        inp = '1111'
        stream.writeBits(int(inp,2) ,4)
        stream.writeAll()
        file = open('out.txt', "rb")
        a = []
        stream.resetAll()
        for i in range(0, 16):
            a.append(stream.readbits(1, file))
        print(a)


if __name__ == "__main__":
    main()
'''
