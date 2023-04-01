import unittest
from PngGenerator import PngBuilder, ColorType
import struct

class PngBuilderRGBTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.imgData = []

        row =0
        while row < 32:
            col = 0
            rowData = []
            while col < 32:
                rowData.append([255,255,255])
                col+=1
            self.imgData.append(rowData)	
            row+=1

        self.photoBuilder = PngBuilder(32,32,ColorType.RGB)
        self.photoBuilder.addIDATChunk(self.imgData)
        
    def test_pngMagicNumberCompliant(self):
        
        data=self.photoBuilder.getFileByteContent()
        self.assertEqual(data[0:8], b'\x89PNG\r\n\x1a\n')
