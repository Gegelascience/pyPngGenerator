
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