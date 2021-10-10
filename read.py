from pyzbar.pyzbar import decode # Libreria para descodificar qr
from PIL import Image # Libreria para trabajar con imagenes


def read_qr(name):
    decoder = decode(Image.open(name))
    return decoder[0].data.decode()
