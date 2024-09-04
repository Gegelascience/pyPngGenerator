from .enumHelper import ColorType
import struct

class Pixel:

    def __init__(self,red:int=0,green:int=0,blue:int=0,alpha:int=255,gray:int=0, paletteCode:int=0):
        if not self.__checkCorrectValue(red):
            raise Exception("invalid red value")
        self.__red = red
        if not self.__checkCorrectValue(green):
            raise Exception("invalid green value")
        self.__green = green
        if not self.__checkCorrectValue(blue):
            raise Exception("invalid blue value")
        self.__blue = blue
        if not self.__checkCorrectValue(gray):
            raise Exception("invalid gray value")
        self.__gray = gray
        
        if not self.__checkCorrectValue(paletteCode):
            raise Exception("invalid gray value")
        self.__palette = paletteCode

        if not self.__checkCorrectValue(alpha):
            raise Exception("invalid alpha value")
        self.__alpha = alpha

    def setRed(self,val:int):
        if self.__checkCorrectValue(val):
            self.__red = val

    def setGreen(self, val:int):
        if self.__checkCorrectValue(val):
            self.__green = val

    def setBlue(self, val:int):
        if self.__checkCorrectValue(val):
            self.__blue = val

    def setGray(self, val:int):
        if self.__checkCorrectValue(val):
            self.__gray = val

    def setPaletteCode(self, val:int):
        if self.__checkCorrectValue(val):
            self.__palette = val

    def setAlpha(self, val:int):
        if self.__checkCorrectValue(val):
            self.__alpha = val

    def __checkCorrectValue(self,val:int):
        return val >=0 and val <=255

    def getPixelData(self,colorMode: ColorType):
        if colorMode == ColorType.RGB:
            return (struct.pack('>B', self.__red), struct.pack('>B', self.__green),struct.pack('>B', self.__blue))
        elif colorMode == ColorType.RGBA:
            return (struct.pack('>B', self.__red), struct.pack('>B', self.__green), struct.pack('>B', self.__blue), struct.pack('>B', self.__alpha))
        elif colorMode == ColorType.GRAYSCALE:
            return (struct.pack('>B', self.__gray),)
        elif colorMode == ColorType.COLORPALLETTE:
            return (struct.pack('>B', self.__palette),)
        elif colorMode == ColorType.GRAYSCALEALPHA:
            return (struct.pack('>B', self.__gray), struct.pack('>B', self.__alpha))
        
class PicturePixels:

    def __init__(self):
        self.__pixelRows:list[list[Pixel]] = []
        self.__lenRow = 0

    def addRow(self,rowPixel:list[Pixel]):
        if self.__lenRow > 0 and len(rowPixel) != self.__lenRow:
            raise Exception("Invalid row, wrong number of pixels")
        if self.__lenRow == 0:
            self.__lenRow = len(rowPixel)
        self.__pixelRows.append(rowPixel)

    def clearPixels(self):
        self.__pixelRows = []

    def getListRowPixels(self):
        return self.__pixelRows

    def getPixelsForPngBuilder(self, colorMode: ColorType):
        listPixels = []
        for row in self.__pixelRows:
            rowPlain = []
            for pixel in row:
                rowPlain.extend(pixel.getPixelData(colorMode))

            listPixels.append(rowPlain)
        
        return listPixels