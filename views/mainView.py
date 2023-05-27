from tkinter import Tk, ttk, PhotoImage,Canvas,filedialog
from tkinter.colorchooser import askcolor
from PngGenerator import PngBuilder, ColorType, SimpleRGBPngBuilder

def generateIconImg() -> PhotoImage:
	iconeData= []

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
		iconeData.append(rowData)	
		row+=1


	pngBuilder = PngBuilder(32,32,ColorType.RGBA )
	pngBuilder.addIDATChunk(iconeData)

	return PhotoImage(data= pngBuilder.getFileByteContent())

def hexaToRGB(hexaValue:str) -> tuple:
	hVal=hexaValue.lstrip('#')
	return tuple(int(hVal[i:i+2], 16) for i in (0, 2, 4))

class MyApp(Tk):
	"""
	App Class
	"""
	def __init__(self):
		super().__init__()
		
		self.title("Png Generator")
		self.geometry('1000x900')
		self.configure(bg='white')

		photo = generateIconImg()
		self.wm_iconphoto(True,photo)

		self.coloringColor =((255,255,255),'#ffffff')

		# input couleur
		ttk.Button(self,text="Select color to apply", command=self.switchColor).grid(column=0,row=0, columnspan=12, sticky="E")
		self.colorPreview = Canvas(self,background='#ffffff' , width=50, height=50,highlightthickness=1)
		self.colorPreview.grid(column=12,row=0, columnspan=12)
		

		# champ de bouton 32x32
		self.imgPixel = []
		for i in range(32):
			line = []
			for j in range(32):
				pixel =Canvas(self,background='#000000' , width=20, height=20)
				pixel.bind("<Button-1>", self.colorCell)
				pixel.grid(column=j+2,row=i+2)
				line.append(pixel)

			self.imgPixel.append(line)

		ttk.Button(self,text="generate png", command=self.writePng).grid(column=24,row=0,columnspan=10)

		# path input
		# validate
		# msg info

	def switchColor(self):
		colors = askcolor(title='Choose a color')
		if colors[0] and colors[1]:
			self.coloringColor =colors
			self.colorPreview.configure(bg=colors[1])


	def colorCell(self,event):
		event.widget.configure(bg=self.coloringColor[1])


	def writePng(self):

		targetFilename = filedialog.asksaveasfilename(filetypes=[("png file","*.png")], defaultextension=".png",initialfile="image.png", title="Generate your picto")
		if targetFilename:

			dataRGBImg = []

			for line in self.imgPixel:
				rowRgb = []
				for pixel in line:
					rowRgb.append(hexaToRGB(pixel["background"]))

				dataRGBImg.append(rowRgb)

			pngBuilder = SimpleRGBPngBuilder(dataRGBImg,32,32)
			pngBuilder.writeFile(targetFilename)
