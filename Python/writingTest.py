testFile = open('text.txt', "wb")
message = "frame1 x1 y1\n".encode('utf-8')

arr = [255,193,2]
testFile.write(message)
testFile.write(bytearray(arr))
testFile.close()

readTest = open('text.txt', "rb")
message = readTest.readline()
print(message.decode('utf-8').rstrip())
print(readTest.readline())