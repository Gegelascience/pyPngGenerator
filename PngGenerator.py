import zlib
import struct
from enum import Enum, IntEnum, unique

@unique
class ColorType(IntEnum):
    RGB = 2
    RGBA = 6

@unique
class TextKeyword(Enum):
	TITLE = "Title"
	AUTHOR = "Author"
	DESC = "Description"
	COPYRIGHT = "Copyright"
	CreaTime = "Creation Time"
	SOFTWARE = "Software"
	DISCLAMER = "Disclaimer"
	WARNING = "Warning"
	SOURCE ="Source"
	COMMENT = "Comment"

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

	def __init__(self,height:int, width:int, colorType:ColorType) -> None:
		
		# magic number
		self.__magicNumber = struct.pack('>BBBBBBBB', 137, 80, 78, 71, 13, 10, 26,10)
		
		# IDHR
		# profondeur 8 bits, rbga (6)
		self.__IDHRChunk = PngChunkBuilder(u'IHDR',struct.pack('>IIBBBBB', width, height, 8, colorType, 0, 0, 0))

		# IDAT chunks init
		self.__IDATChunks:list[PngChunkBuilder] = []


		# tEXt chunks init
		self.__tEXtChunks:list[PngChunkBuilder] = []		

		# IEND chunk
		self.__IENDChunk=PngChunkBuilder(u'IEND',"")

	def addIDATChunk(self,data:list[list[tuple]]):
		image = []

		for ligne in data:
			image.append(0)
			ligneInt = []
			for pixel in ligne:
				ligneInt.extend(pixel)
			image.extend(ligneInt)

		image_compressee = zlib.compress(bytearray(image))

		self.__IDATChunks.append(PngChunkBuilder(u'IDAT',image_compressee))


	def addtEXtChunk(self,keyword:TextKeyword,data:str):
		self.__tEXtChunks.append(PngChunkBuilder(u'tEXt',struct.pack('>' + str(len(keyword.value)) +  'sB' + str(len(data)) + 's' ,str(keyword.value).encode('latin1'),0,data.encode('latin1'))))

	def removelastIDATChunk(self):
		self.__IDATChunks.pop()	
	
	def removelasttExtChunk(self):
		self.__tEXtChunks.pop()	


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


