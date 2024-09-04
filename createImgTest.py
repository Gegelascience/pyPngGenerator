from PngGenerator import PngBuilder, ColorType, TextKeyword, PhysicalPixelSizeUnit, Pixel, PicturePixels

def createRGBPng(filename):
	test2 = PicturePixels()

	row =0
	while row < 32:
		col = 0
		rowData = []
		while col < 32:
			if row > 2 and row <29 and (col in [4,5,6,25,26,27] or ((col==row or col == row+1 or col == row-1) and col > 3 and col <28)):

				rowData.append(Pixel(255,255,255))
			else:
				rowData.append(Pixel(255,0,0))
			col+=1
		test2.addRow(rowData)	
		row+=1

	pngBuilder2 = PngBuilder(32,32,ColorType.RGB)
	pngBuilder2.addIDATChunk(test2)
	pngBuilder2.settRNSChunk([255,255,255])

	pngBuilder2.setbKGDChunk([0,0,255])

	pngBuilder2.setcHRMChunk(0,0,0.5,0.5,0.8,0.8,0.2,0.2)
	pngBuilder2.setpHYsChunk(3,1,PhysicalPixelSizeUnit.METER)
	pngBuilder2.setsBITChunk([7,7,7])

	pngBuilder2.addtEXtChunk(TextKeyword.AUTHOR,"gegelascience")
	pngBuilder2.addzTXtChunk(TextKeyword.COMMENT,"Ceci est un commentaire")
	pngBuilder2.writeFile(filename)

	print(pngBuilder2.getBase64ContentValue())
	print(pngBuilder2.getBase64ContentValue(True))



def createRGBAPng(filename):
	test= PicturePixels()

	row =0
	while row < 32:
		col = 0
		rowData = []
		while col < 32:
			if row < 16 and col < 16 :

				rowData.append(Pixel(255,0,0,255))
			elif row < 16 and col >= 16:
				rowData.append(Pixel(0,255,0,255))
			elif row >= 16 and col >= 16:
				rowData.append(Pixel(0,0,255,255))
			else:
				rowData.append(Pixel(255,255,255,255))
			col+=1
		test.addRow(rowData)	
		row+=1


	pngBuilder = PngBuilder(32,32,ColorType.RGBA )
	pngBuilder.addIDATChunk(test)
	pngBuilder.setcHRMChunk(0,0,0.5,0.5,0.8,0.8,0.2,0.2)
	pngBuilder.setgAMAChunk(0.45)
	pngBuilder.setpHYsChunk(1,1,PhysicalPixelSizeUnit.UNKNOWN)
	pngBuilder.addtEXtChunk(TextKeyword.AUTHOR,"gegelascience")
	pngBuilder.addtEXtChunk(TextKeyword.SOFTWARE,"python 3")
	pngBuilder.writeFile(filename)


def createPaletteRGBPng(filename):

	test3 = PicturePixels()

	paletteData = [
		(255,0,0),
		(0,255,0),
		(0,0,255),
		(255,255,255)
	]

	histoData = [
		8,8,8,8
	]

	transparencyIndex = [
		255,0,0,255
	]

	row =0
	while row < 32:
		col = 0
		rowData = []
		while col < 32:
			if row < 16 and col < 16 :

				rowData.append(Pixel(paletteCode=0))
			elif row < 16 and col >= 16:
				rowData.append(Pixel(paletteCode=1))
			elif row >= 16 and col >= 16:
				rowData.append(Pixel(paletteCode=2))
			else:
				rowData.append(Pixel(paletteCode=3))

			col+=1
		test3.addRow(rowData)	
		row+=1

	pngBuilder3 = PngBuilder(32,32,ColorType.COLORPALLETTE)
	pngBuilder3.addIDATChunk(test3)
	pngBuilder3.setPLTEChunkAndhISTChunk(paletteData,histoData)

	pngBuilder3.settRNSChunk(transparencyIndex)
	
	pngBuilder3.addtEXtChunk(TextKeyword.AUTHOR,"gegelascience")
	pngBuilder3.writeFile(filename)

if __name__ == "__main__":
	createRGBPng("testRGB.png")
	createRGBAPng("testRGBA.png")
	createPaletteRGBPng("testPaletteRGB.png")