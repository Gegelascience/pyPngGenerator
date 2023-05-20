from tkinter import Tk, ttk, PhotoImage
from tkinter.colorchooser import askcolor
from PngGenerator import PngBuilder, ColorType

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

class MyApp(Tk):
	"""
	App Class
	"""
	def __init__(self):
		super().__init__()
		
		self.title("Png Generator")
		self.geometry('600x800')
		self.configure(bg='white')

		photo = generateIconImg()
		self.wm_iconphoto(True,photo)

		# input couleur
		ttk.Button(self,text="Select color to apply", command=self.switchColor).pack()

		# champ de bouton 32x32

		# path input
		# validate
		# msg info

	def switchColor(self):
		colors = askcolor(title='Choose a color')
		print(colors)

