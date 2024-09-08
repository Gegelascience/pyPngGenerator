from wsgiref.simple_server import make_server
from urllib.parse import parse_qsl
import json
from PngGenerator import PngBuilder, ColorType, TextKeyword, PhysicalPixelSizeUnit, Pixel, PicturePixels

def simple_app(environ, start_response):
    
    
    if environ['REQUEST_METHOD'] == 'POST':
        #body
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            if isinstance(request_body,bytes):
                bodyContentStr =request_body.decode("utf-8")

                dataBody  =json.loads(bodyContentStr)

                if isinstance(dataBody,dict):
                    dataPng = dataBody.get("picture",[])
                    
                    height = len(dataPng)
                    if height > 0:
                        width = len(dataPng[0])
                        if width > 0:
                            pngContent = PicturePixels()
                            for row in dataPng:
                                rowPixels = []
                                for pixelJson in row:
                                    if isinstance(pixelJson,dict):
                                        rowPixels.append(Pixel(pixelJson.get("r",0),pixelJson.get("g",0),pixelJson.get("b",0),pixelJson.get("a",255)))
                                pngContent.addRow(rowPixels)

                            pngBuilder = PngBuilder(height,width,ColorType.RGBA)
                            pngBuilder.addIDATChunk(pngContent)
                            binaryContent = pngBuilder.getFileByteContent()

                            filename = dataBody.get("name","filename.png")

                            status = '200 OK'
                            headers = [
                                ('Content-Type', 'image/png'),
                                ('Content-Length',str(len(binaryContent))),
                                ('Content-Disposition','attachment; filename="'+ filename +'"')
                                ]
        
                            start_response(status, headers)
                            return [binaryContent]
                        
            status = '400 Bad Request'
            headers = [('Content-Type', 'text/plain')]

            resultBody = 'Invalid Request'

            start_response(status, headers)
            return [ stringData.encode() for stringData in resultBody ]
        except Exception as ex:

            print(ex)

            status = '400 Bad Request'
            headers = [('Content-Type', 'text/plain')]

            resultBody = 'Invalid Request'

            start_response(status, headers)
            return [ stringData.encode() for stringData in resultBody ]

        # query string
        #queryString = parse_qsl(environ['QUERY_STRING'])  # turns the qs to a dict
        
    

    else:  # GET
        queryString = parse_qsl(environ['QUERY_STRING'])

        resultBody = 'From GET: %s' % ''.join('%s: %s' % (k, v) for k, v in queryString)
        status = '200 OK'
        headers = [('Content-Type', 'text/plain')]
    
        start_response(status, headers)
        return [ stringData.encode() for stringData in resultBody ]


with make_server('', 8000, simple_app) as httpd:
    print("Serving HTTP on port 8000...")

    # Respond to requests until process is killed
    httpd.serve_forever()

    # Alternative: serve one request, then exit
    #httpd.handle_request()