from PIL import Image
import numpy as np
from Golomb import Golomb
from BitStream import Stream
import time

class Block:
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.space = np.zeros((self.width, self.height), dtype = np.uint8)

	def setData(self, i, j, data):
		self.space[i][j] = data

	def getData(self, i, j):
		return self.space[i][j]

class TimeEncoder:
	def __init__(self, filename, mode):
		self.filename = filename
		self.mode = mode
		self.width = 720
		self.height = 1280
		self.frame_len = 0
		self.bStream = Stream()
		self.gol = Golomb(4)
		self.totalTime = 0

	def encode(self):
		f=open(self.filename, "rb")
		frame = f.readline().decode('utf-8')
		rgb = np.zeros((self.height, self.width, 3), dtype=np.uint8)
		blockMatrix = [[[Block(8,8) for a in range(0, 160)] for b in range(0, 90)] for c in range(0, 3)]
		if self.mode == '4:4:4':
			#for r in range(0, 2):
					self.frame_len = self.width*self.height*3
					x = f.readline()
					raw = f.read(self.frame_len)
					y = np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height)
					u= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height)
					v= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height*2)
					y = y.reshape(self.width,self.height)
					u=u.reshape(self.width,self.height)
					v=v.reshape(self.width,self.height)
					for z in range(0, 3):
						if z == 0:
							self.bStream.setMatrix('y')
							cMatrix = y
						elif z == 1:
							self.bStream.setMatrix('u')
							cMatrix = u
						else:
							self.bStream.setMatrix('v')
							cMatrix = v
						for i in range(0, 90):
							for j in range(0, 160):
								refBlock = blockMatrix[z][i][j]
								flag = True
								for l in range(0, 8):
									for m in range(0, 8):
										w = int(l + i*8)
										h = int(m + j*8)
										if refBlock.getData(l,m) != cMatrix[w][h] and flag:
											flag = False
											l = 0
											m = 0
										if not flag:
											block = Block(8,8)
											x = int(cMatrix[w][h])
											p = int(self.predictor(cMatrix, w, h, '1'))
											e = x - p
											if e < 0:
												e = 2*abs(e) - 1
											else:
												e = 2*e
											enc = self.gol.encode(e)
											nu = ''.join(str(e) for e in enc)
											self.bStream.writeBits(int(nu, 2), len(enc))
											block.setData(l, m, x)
								if not flag:
									blockMatrix[0][i][j] = block
					self.bStream.writeAll('timeOut.txt')
					self.bStream.resetAll()

	def decode(self):
		pass

	def predictor(self,matrix, i, j, tipo):
		a = 0
		b = 0
		c = 0
		if tipo == '1':
			if j > 0:
				return matrix[i][j-1]
			return 0
		elif tipo == '2':
			if i > 0:
				return matrix[i-1][j]
			return 0
		elif tipo == '3':
			if i > 0 and j > 0:
				return matrix[i-1][j-1]
			return 0
		else:
			if j > 0:
				a = matrix[i][j-1]
				if i > 0:
					b = matrix[i-1][j]
					c = matrix[i-1][j-1]
			elif i > 0:
				b = matrix[i-1][j]
			if tipo == '4':
				return a + b -c
			elif tipo == '5':
				return a + (b-c)/2
			elif tipo == '6':
				return b + (a-c)/2
			elif tipo == '7':
				return (a+b)/2
			elif tipo == 'jpegLS':
				if c >= max(a,b):
					return min(a,b)
				elif c <= min(a,b):
					return max(a,b)
				else:
					return int(a)+int(b)-int(c)