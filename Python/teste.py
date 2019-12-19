from BitStream import Stream

bS = Stream()

ch = '001100101'

for c in ch:
    a  = bS.writeBits(ord(c),1)
print(a)


#c = int('001100101',2)
#bS.writeBits(c, 9, 'out')


chars = []
x = bS.readbits(8, a)
chars.append(chr(x))
print(''.join(chars))
