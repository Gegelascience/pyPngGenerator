
from enum import Enum, IntEnum, unique

@unique
class ColorType(IntEnum):
    GRAYSCALE = 0
    RGB = 2
    COLORPALLETTE= 3
    GRAYSCALEALPHA = 4
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
        
@unique
class PhysicalPixelSizeUnit(IntEnum):
    UNKNOWN = 0
    METER = 1
      
@unique
class PngChunkName(Enum):
	IHDR="IHDR"
	IDAT="IDAT"
	IEND="IEND"
	tIME="tIME"
	tEXt="tEXt"
	zTXt="zTXt"
	PLTE="PLTE"
	hIST="hIST"
	tRNS="tRNS"
	bKGD="bKGD"
	cHRM="cHRM"
	gAMA="gAMA"
	pHYs="pHYs"
	sBIT="sBIT"