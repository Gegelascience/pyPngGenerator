from PngGenerator import PngBuilder

if __name__ == "__main__":

	test= [
		[ (255, 0, 0,255),(0, 255, 0,255)],
		[ (0, 0, 255,255),(255, 255, 255,255)],
		[ (0, 0, 0,255),(0, 0, 0,255)],
		[ (0, 0, 0,255),(0, 0, 0,255)],
	]
	pngBuilder = PngBuilder(test,4,2)
	pngBuilder.writeFile("test.png")