from PngGenerator import PngBuilder, ColorType, TextKeyword

if __name__ == "__main__":

	# RGBA
	test= []

	row =0
	while row < 32:
		col = 0
		rowData = []
		while col < 32:
			if row < 16 and col < 16 :

				rowData.append([255,0,0,255])
			elif row < 16 and col >= 16:
				rowData.append([0,255,0,255])
			elif row >= 16 and col >= 16:
				rowData.append([0,0,255,255])
			else:
				rowData.append([255,255,255,255])
			col+=1
		test.append(rowData)	
		row+=1


	pngBuilder = PngBuilder(32,32,ColorType.RGBA )
	pngBuilder.addIDATChunk(test)
	pngBuilder.addtEXtChunk(TextKeyword.AUTHOR,"gegelascience")
	pngBuilder.addtEXtChunk(TextKeyword.SOFTWARE,"python 3")
	pngBuilder.writeFile("test.png")


	# RGB
	test2 = []

	row =0
	while row < 32:
		col = 0
		rowData = []
		while col < 32:
			if row > 2 and row <29 and (col in [4,5,6,25,26,27] or ((col==row or col == row+1 or col == row-1) and col > 3 and col <28)):

				rowData.append([255,255,255])
			else:
				rowData.append([255,0,0])
			col+=1
		test2.append(rowData)	
		row+=1

	pngBuilder2 = PngBuilder(32,32,ColorType.RGB)
	pngBuilder2.addIDATChunk(test2)
	pngBuilder2.addtEXtChunk(TextKeyword.AUTHOR,"gegelascience")
	pngBuilder2.writeFile("test2.png")

	# Palette

	test3 = []

	paletteData = [
		(255,0,0),
		(0,255,0),
		(0,0,255),
		(255,255,255)
	]

	row =0
	while row < 32:
		col = 0
		rowData = []
		while col < 32:
			if row < 16 and col < 16 :

				rowData.append([0])
			elif row < 16 and col >= 16:
				rowData.append([1])
			elif row >= 16 and col >= 16:
				rowData.append([2])
			else:
				rowData.append([3])

			col+=1
		test3.append(rowData)	
		row+=1

	pngBuilder3 = PngBuilder(32,32,ColorType.COLORPALLETTE)
	pngBuilder3.addIDATChunk(test3)
	pngBuilder3.setPLTEChunk(paletteData)
	
	pngBuilder3.addtEXtChunk(TextKeyword.AUTHOR,"gegelascience")
	pngBuilder3.writeFile("test3.png")