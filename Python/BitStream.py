import time
##Documentation for the Bitstream class
#
#Class with the objectives: 
# Receiving data from outside source, 
# Storing it as a value between 0 and 255,
# Writing all data into a file,
# Reading data from a file,
# Returning said data as a value between 0 and 255

class Stream(object):

    def __init__(self):
        self.accumulator = 0
        self.bcount = 0
        self.y = []
        self.u = []
        self.v = []
        self.matrix = ''

##Function that writes a single bit
#   Requires a 'bit'
#   If bcount is 8 then all the information stored on the accumulator will be stored on the current matrix being used by the Encoder class, and both the bcount and accumulator will be reset back to 0
#   If the 'bit' is 1 it will be added to the accumulator
#   bcount will be incremented every time this function is used
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

##Function n bits
#This function requires a number and the number os bits that number has
#Transformes the number in bits to 1s or 0s
#Calls writeBits n times 
    def writeBits(self, bits, n):
        while n > 0:
            self.writeBit(bits & 1 << n-1)
            n -= 1

##Function that writes all info stored on the BitStream
#All data is stored in 3 different matrixes, after a frame has been fully loaded this function is used to write everything on a file
    def writeAll(self , outFile):
        file = open(outFile, 'ab')
        for data in self.y:
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

##Function that reads a bit from a file and return it to who called it
    def readbit(self, file):
        if not self.bcount:
            a = file.read(1)
            if a:
                self.accumulator = ord(a)
            self.bcount = 8
            #self.read = len(a)
        rv = (self.accumulator & (1 << self.bcount-1)) >> self.bcount-1
        self.bcount -= 1
        return rv

##Function that resets the information to prepare for the next frame
    def resetAll(self):
        self.accumulator = 0
        self.bcount = 0

##Function that reads multiple bits from a file
#Sends to readbit the file to read and after n iteratons returns the value
    def readbits(self, n, nFile):
        file = nFile
        v = 0
        while n > 0:
            v = (v << 1) | self.readbit(file)
            n -= 1
        return v

##Function that determines which frame component it should store information
    def setMatrix(self, matrix):
        self.matrix = matrix
