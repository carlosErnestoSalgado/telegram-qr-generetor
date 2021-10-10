Read one-dimensional barcodes and QR codes from Python 2 and 3 using the zbar library.
    Pure python
    Works with PIL / Pillow images, OpenCV / numpy ndarrays, and raw bytes
    Decodes locations of barcodes
    No dependencies, other than the zbar library itself
    Tested on Python 2.7, and Python 3.4 to 3.6

The older zbar package is stuck in Python 2.x-land. 
The zbarlight package does not provide support for Windows and depends upon Pillow.
Install
pip install pyzbar
The decode function accepts instances of PIL.Image.

>>> from pyzbar.pyzbar import decode
>>> from PIL import Image
>>> decode(Image.open('pyzbar/tests/code128.png'))
[
    Decoded(
        data=b'Foramenifera', type='CODE128',
        rect=Rect(left=37, top=550, width=324, height=76),
        polygon=[
            Point(x=37, y=551), Point(x=37, y=625), Point(x=361, y=626),
            Point(x=361, y=550)
        ]
    )
    Decoded(
        data=b'Rana temporaria', type='CODE128',
        rect=Rect(left=4, top=0, width=390, height=76),
        polygon=[
            Point(x=4, y=1), Point(x=4, y=75), Point(x=394, y=76),
            Point(x=394, y=0)
        ]
    )
]
