import math


'''def main():

    #Use example of the slides
    golomb = Golomb(4)
    l=golomb.encode(11)
    print (l)

    x=golomb.decode(l)
    print (x)



'''
class Golomb:
    def __init__(self,m):
        self.m = m
        self.b = math.ceil(math.log2(m))

    def encode(self, number):
        (q, r)=divmod(number, self.m)
        #Write number of '1' equal to the number of quocient and add a zero
        ret=[]
        for i in range(q):
            ret.append(1)
        ret.append(0)
        #For the r, it is represented by the binary code
        for i in range(self.b-1, -1, -1):
            bit=(r >> i) & 1
            ret.append(bit)
        return ret

    def decode(self, codigo):
        q = 0
        while codigo.pop(0):
            q+=1
        r = 0
        for i in range(self.b-1, -1, -1):
            bit = codigo.pop(0)
            r += int(bit) << i

        return q*self.m + r


#main()
