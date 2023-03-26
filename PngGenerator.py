import zlib
import struct

class PngChunkBuilder:

	def __init__(self,chunkName:str,data:bytes):
		self.__chunkType = chunkName.encode("ascii")
		if chunkName != "IEND":
			self.__chunkData = data
			self.__chunkDataLen = struct.pack('>I', len(data))
		else:
			self.__chunkData= "".encode()
			self.__chunkDataLen =struct.pack('>I', 0)
		self.__chunkCRC = struct.pack('>I', zlib.crc32(self.__chunkData, zlib.crc32(struct.pack('>4s', self.__chunkType))))

	def getBytesContent(self):
		return b"".join([self.__chunkDataLen,self.__chunkType, self.__chunkData, self.__chunkCRC])


class PngBuilder:

	def __init__(self,height:int, width:int) -> None:
		
		# magic number
		self.__magicNumber = struct.pack('>BBBBBBBB', 137, 80, 78, 71, 13, 10, 26,10)
		
		# IDHR
		# profondeur 8 bits, rbga (6)
		self.__IDHRChunk = PngChunkBuilder(u'IHDR',struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))

		# IDAT chunks init
		self.__IDATChunks:list[PngChunkBuilder] = []


		# tEXt chunks init
		self.__tEXtChunks:list[PngChunkBuilder] = []		

		# IEND chunk
		self.__IENDChunk=PngChunkBuilder(u'IEND',"")

	def addIDATChunk(self,data):
		image = []

		for ligne in data:
			image.append(0)
			ligneInt = []
			for pixel in ligne:
				ligneInt.extend(pixel)
			image.extend(ligneInt)

		image_compressee = zlib.compress(bytearray(image))

		self.__IDATChunks.append(PngChunkBuilder(u'IDAT',image_compressee))


	def addtEXtChunk(self,keyword:str,data:str):

		listAcceptedKeyword = [
			"Title",
			"Author",
			"Description",
			"Copyright",
			"Creation Time",
			"Software",
			"Disclaimer",
			"Warning",
			"Source",
			"Comment"
		]

		if keyword not in listAcceptedKeyword:
			raise Exception("Invalid keyword, "  + keyword + " not supported")
		self.__tEXtChunks.append(PngChunkBuilder(u'tEXt',struct.pack('>6sB' + str(len(data)) + 's' ,keyword.encode('latin1'),0,data.encode('latin1'))))
		

	def getFileByteContent(self):
		byteContentList: list[bytes] = []

		byteContentList.append(self.__magicNumber)
		byteContentList.append(self.__IDHRChunk.getBytesContent())
		byteContentList.extend([iData.getBytesContent() for iData in self.__IDATChunks])
		byteContentList.extend([txtChunk.getBytesContent() for txtChunk in self.__tEXtChunks])
		byteContentList.append(self.__IENDChunk.getBytesContent())

		return b"".join(byteContentList)

	def writeFile(self,filePath:str):
		binaryFileContent = self.getFileByteContent()
		with open(filePath,"wb") as pngFile:
			pngFile.write(binaryFileContent)


