import zlib
import struct
from datetime import datetime
from PngGenerator import ColorType, TextKeyword, PhysicalPixelSizeUnit
import math
import base64


class PngChunkBuilder:

	def __init__(self,chunkName:str,data:bytes):
		self.__chunkType = chunkName.encode("ascii")
		if chunkName != "IEND":
			self.__chunkData = data
			self.__chunkDataLen = struct.pack('>I', len(data))
			if chunkName =="PLTE" and len(data)%3 !=0:
				raise Exception("invalid palette data")
		else:
			self.__chunkData= "".encode()
			self.__chunkDataLen =struct.pack('>I', 0)
		self.__chunkCRC = struct.pack('>I', zlib.crc32(self.__chunkData, zlib.crc32(struct.pack('>4s', self.__chunkType))))

	def getBytesContent(self):
		return b"".join([self.__chunkDataLen,self.__chunkType, self.__chunkData, self.__chunkCRC])


class PngBuilder:

	def __init__(self,height:int, width:int, colorType:ColorType) -> None:
		
		# magic number
		self.__magicNumber = struct.pack('>BBBBBBBB', 137, 80, 78, 71, 13, 10, 26,10)
		
		# IDHR
		# profondeur 8 bits, rbga (6)
		self.__IDHRChunk = PngChunkBuilder(u'IHDR',struct.pack('>IIBBBBB', width, height, 8, colorType, 0, 0, 0))

		self.__bitDepth = 8

		# PLTE chunk init
		self.__PLTEChunk = None
		self.__mandatoryPlte = False
		self.__colorType = colorType
		if colorType == ColorType.COLORPALLETTE:
			self.__mandatoryPlte = True

		# self.__hISTChunk init
		self.__hISTChunk = None

		# tRNS chunk init
		self.__tRNSChunk = None

		# bKGD chunk init
		self.__bKGDChunk = None

		# cHRM chunk init
		self.__cHRMChunk = None

		# gAMA chunk init
		self.__gAMAChunk = None

		# pHYs chunk init
		self.__pHYsChunk = None

		# sBIT chunk
		self.__sBITChunk = None

		# IDAT chunks init
		self.__IDATChunks:list[PngChunkBuilder] = []

		# tIME chunk init
		self.__tIMEChunk = None

		# tEXt chunks init
		self.__tEXtChunks:list[PngChunkBuilder] = []

		# zTxt chunk init
		self.__zTXtChunks:list[PngChunkBuilder] = []

		# IEND chunk
		self.__IENDChunk=PngChunkBuilder(u'IEND',b"")

	def addIDATChunk(self,data:list[list[tuple]]):
		image = []

		for ligne in data:
			image.append(struct.pack('>B', 0))
			ligneInt = []
			for pixel in ligne:
				for color in pixel:
					ligneInt.append(struct.pack('>B', color))
			image.extend(ligneInt)

		image_compressee = zlib.compress(b"".join(image))

		self.__IDATChunks.append(PngChunkBuilder(u'IDAT',image_compressee))


	def addtEXtChunk(self,keyword:TextKeyword,data:str):
		self.__tEXtChunks.append(PngChunkBuilder(u'tEXt',struct.pack('>' + str(len(keyword.value)) +  'sB' + str(len(data)) + 's' ,str(keyword.value).encode('latin1'),0,data.encode('latin1'))))

	def addzTXtChunk(self,keyword:TextKeyword,data:str):
		keywordAndNullCharBinary = struct.pack('>' + str(len(keyword.value)) +  'sBB',str(keyword.value).encode('latin1'),0,0)
		dataCompress = zlib.compress(data.encode('latin1'))
		self.__zTXtChunks.append(PngChunkBuilder(u'zTXt',b"".join([keywordAndNullCharBinary, dataCompress])))
	
	def setPLTEChunkAndhISTChunk(self,paletteData:list[tuple],histoData: list[int]= []):
		listEntriesPalette = []
		if self.__colorType == ColorType.GRAYSCALE or self.__colorType == ColorType.GRAYSCALEALPHA:
			raise Exception("PLTE invalid with grayscale modes")
		
		if len(paletteData) > 0:
			for entry in paletteData:
				for color in entry:
					listEntriesPalette.append(struct.pack('>B', color))
			self.__PLTEChunk = PngChunkBuilder(u'PLTE', b"".join(listEntriesPalette))

		listEntriesHisto = []
		if len(paletteData) > 0 and len(histoData) > 0:
			for entry in histoData:
				listEntriesHisto.append(struct.pack('>H', entry))

			self.__hISTChunk = PngChunkBuilder(u'hIST', b"".join(listEntriesHisto))

	
	def settRNSChunk(self,chunkData:list):
		listEntries = []
		if self.__colorType == ColorType.GRAYSCALEALPHA or self.__colorType == ColorType.RGBA:
			raise Exception("tRNS invalid with alpha data in IDAT chunks")
		
		if self.__colorType == ColorType.COLORPALLETTE:
			for indexTransparency in chunkData:
				listEntries.append(struct.pack('>B', indexTransparency))

		
		elif self.__colorType == ColorType.GRAYSCALE or self.__colorType == ColorType.RGB:
			for colorTransparency in chunkData:
				listEntries.append(struct.pack('>h', colorTransparency))


		self.__tRNSChunk = PngChunkBuilder(u'tRNS', b"".join(listEntries))


	def setbKGDChunk(self,chunkData:list):
		listEntries = []
		if self.__colorType != ColorType.COLORPALLETTE:
			for entry in chunkData:
				listEntries.append(struct.pack('>h', entry))
		else:
			listEntries.append(struct.pack('>B', chunkData[0]))

		self.__bKGDChunk = PngChunkBuilder(u'bKGD', b"".join(listEntries))

	def setcHRMChunk(self, xWhite:float,yWhite:float,xRed:float,yRed:float, xGreen:float, yGreen:float, xBlue:float, yBlue:float):
		listOriginalCoord = [xWhite,yWhite,xRed,yRed, xGreen, yGreen, xBlue, yBlue]
		listFormatedCoord = []
		for coord in listOriginalCoord:
			if coord <= 1 and coord >= 0:
				listFormatedCoord.append(struct.pack('>I', math.trunc(coord*100000)))
			else:
				raise Exception("Invalid Chromatic Coordonate, must be between 0 and 1")
			
		self.__cHRMChunk = PngChunkBuilder(u'cHRM', b"".join(listFormatedCoord))

	def setgAMAChunk(self,gamaValue:float):
		if gamaValue <= 1 and gamaValue >= 0:
				formatedGamma = struct.pack('>I', math.trunc(gamaValue*100000))
		else:
			raise Exception("Invalid Gamma, must be between 0 and 1")
		self.__gAMAChunk = PngChunkBuilder(u'gAMA', formatedGamma)


	def setpHYsChunk(self, horizontalNbPixel:int, verticalNbPixel:int, unit: PhysicalPixelSizeUnit):
		self.__pHYsChunk = PngChunkBuilder(u'pHYs',struct.pack('>IIB', horizontalNbPixel,verticalNbPixel,unit))

	def setsBITChunk(self, chunkData:list[int]):
		listEntries = []
		for entry in chunkData:
			if entry > 0 and entry < self.__bitDepth: 
				listEntries.append(struct.pack('>B', entry))
			else:
				raise Exception("Invalid bit depth")
		self.__sBITChunk = PngChunkBuilder(u'sBIT',b"".join(listEntries))

	
	def removelastIDATChunk(self):
		self.__IDATChunks.pop()	
	
	def removelasttExtChunk(self):
		self.__tEXtChunks.pop()	

	def removelastzTxtChunk(self):
		self.__zTXtChunks.pop()	

	def removegAMAChunk(self):
		self.__gAMAChunk = None

	def removetRNSChunk(self):
		self.__tRNSChunk = None

	def removebKGDChunk(self):
		self.__bKGDChunk = None

	def removecHRMChunk(self):
		self.__cHRMChunk = None

	def removePLTEChunk(self):
		self.__PLTEChunk = None

	def removehISTChunk(self):
		self.__hISTChunk = None


	def removesBITChunk(self):
		self.__sBITChunk = None

	def removepHYsChunk(self):
		self.__pHYsChunk = None



	def getFileByteContent(self):
		byteContentList: list[bytes] = []

		now = datetime.now()
		now.year
		byteTime = struct.pack('>hBBBBB', now.year,now.month, now.day, now.hour, now.minute, now.second)
		self.__tIMEChunk = PngChunkBuilder(u'tIME', byteTime)

		byteContentList.append(self.__magicNumber)
		byteContentList.append(self.__IDHRChunk.getBytesContent())

		if self.__cHRMChunk:
			byteContentList.append(self.__cHRMChunk.getBytesContent())

		if self.__gAMAChunk:
			byteContentList.append(self.__gAMAChunk.getBytesContent())

		if self.__sBITChunk:
			byteContentList.append(self.__sBITChunk.getBytesContent())

		if self.__PLTEChunk:
			byteContentList.append(self.__PLTEChunk.getBytesContent())

		if self.__mandatoryPlte and not self.__PLTEChunk:
			raise Exception("PLTE chunk missing")
		
		if self.__PLTEChunk and self.__hISTChunk:
			byteContentList.append(self.__hISTChunk.getBytesContent())
		
		if self.__tRNSChunk:
			byteContentList.append(self.__tRNSChunk.getBytesContent())

		if self.__bKGDChunk:
			byteContentList.append(self.__bKGDChunk.getBytesContent())

		if self.__pHYsChunk:
			byteContentList.append(self.__pHYsChunk.getBytesContent())


		byteContentList.extend([iData.getBytesContent() for iData in self.__IDATChunks])

		byteContentList.append(self.__tIMEChunk.getBytesContent())

		byteContentList.extend([txtChunk.getBytesContent() for txtChunk in self.__tEXtChunks])
		byteContentList.extend([ztxtChunk.getBytesContent() for ztxtChunk in self.__zTXtChunks])
		byteContentList.append(self.__IENDChunk.getBytesContent())

		return b"".join(byteContentList)

	def getBase64ContentValue(self):
		binaryFileContent = self.getFileByteContent()
		return base64.b64encode(binaryFileContent).decode()

	def writeFile(self,filePath:str):
		binaryFileContent = self.getFileByteContent()
		with open(filePath,"wb") as pngFile:
			pngFile.write(binaryFileContent)


