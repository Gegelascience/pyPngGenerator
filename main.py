from PngGenerator import PngBuilder

if __name__ == "__main__":

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


	pngBuilder = PngBuilder(test,32,32)
	pngBuilder.writeFile("test.png")


	test2 = []

	row =0
	while row < 32:
		col = 0
		rowData = []
		while col < 32:
			if row > 2 and row <29 and (col in [4,5,6,25,26,27] or col==row or col == row+1 or col == row-1):

				rowData.append([255,255,255,255])
			else:
				rowData.append([255,0,0,255])
			col+=1
		test2.append(rowData)	
		row+=1

	pngBuilder = PngBuilder(test2,32,32)
	pngBuilder.writeFile("test2.png")