class Stream(object):

    def __init__(self, out, input):
        self.accumulator = 0
        self.bcount = 0
        self.out = out
        self.input = input
        

    def writeBit(self, bit):
        if self.bcount == 7:
            self.flush()
            #print("ol")
        if bit > 0:
            self.accumulator |= 1 << 7-self.bcount
        self.bcount +=1
        #print(self.bcount)
    
    def writeBits(self, bits, n):
        while n > 0:
            self.writeBit(bits & 1 << n-1)
            n -= 1

    def flush(self):
        self.out.write(bytearray([self.accumulator]))
        self.accumulator = 0
        self.bcount = 0

    
    def _readbit(self):
        if not self.bcount:
            a = self.input.read(1)
            if a:
                self.accumulator = ord(a)
            self.bcount = 8
            self.read = len(a)
        rv = (self.accumulator & (1 << self.bcount-1)) >> self.bcount-1
        self.bcount -= 1
        return rv

    def readbits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self._readbit()
            n -= 1
        return v