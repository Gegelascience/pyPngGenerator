import zlib
import struct

class PngBuilder:
	binaryContent:bytes

	def __init__(self,rawData,height:int, width:int) -> None:
		
		pngBytesNearlyOK = []

		# magic number
		pngBytesNearlyOK.extend(struct.pack('>BBBBBBBB', 137, 80, 78, 71, 13, 10, 26,10))
		
		# IDHR
		IHDR = ['', '', '', ''] # Les 4 éléments d'un bloc
		IHDR[1] = u'IHDR'.encode('ascii')
		IHDR[2] = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
		IHDR[0] = struct.pack('>I', len(IHDR[2]))
		IHDR[3] = struct.pack('>I', zlib.crc32(IHDR[2], zlib.crc32(struct.pack('>4s', u'IHDR'.encode('ascii')))))

		pngBytesNearlyOK.extend(IHDR)

		# IDAT
		image = []

		for ligne in rawData:
			image.append(0)
			ligneInt = []
			for pixel in ligne:
				ligneInt.extend(pixel)
			image.extend(ligneInt)

		image_compressee = zlib.compress(bytearray(image))

		
		IDAT = ['', '', '', '']
		IDAT[1] = u'IDAT'.encode('ascii')
		IDAT[2] = image_compressee
		IDAT[0] = struct.pack('>I', len(IDAT[2]))
		IDAT[3] = struct.pack('>I', zlib.crc32(IDAT[2], zlib.crc32(struct.pack('>4s', u'IDAT'.encode('ascii')))))

		pngBytesNearlyOK.extend(IDAT)

		# IEND
		IEND = ['', '', '', '']
		IEND[1] = u'IEND'.encode('ascii')
		IEND[0] = struct.pack('>I', len(IEND[2]))
		IEND[3] = struct.pack('>I', zlib.crc32(IEND[2].encode(), zlib.crc32(struct.pack('>4s', u'IEND'.encode('ascii')))))
		
		pngBytesNearlyOK.extend(IEND)


		# formatage du contenu en bytes

		byteContentList = []
		for el in pngBytesNearlyOK:
			if isinstance(el,int):
				byteContentList.append(el.to_bytes(1, byteorder='little'))
			elif isinstance(el,str):
				if len(el) > 0:
					byteContentList.append(bytearray(el,encoding="utf-8"))
			else:
				byteContentList.append(el)

		self.binaryContent = b"".join(byteContentList)


	def writeFile(self,filePath:str):
		with open(filePath,"wb") as pngFile:
			pngFile.write(self.binaryContent)


