import qrcode
from pyzbar.pyzbar import decode # Libreria para descodificar qr
from PIL import Image # Libreria para trabajar con imagenes
import os
from telegram import ChatAction
from telegram.chat import Chat

# Funciones para generaracion de codigo Qr
def generetor_qr(text):
    file_name = text + '.jpg'
    
    img = qrcode.make(text)
    
    img.save(file_name)
    
    return file_name
    
def send_file(filename, chat: Chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_photo(
        photo=open(filename, 'rb')
    )
    os.unlink(filename)
    
# Funciones para la lectura de Qr
def read_qr(text):
    decoder = decode(Image.open(text))
    os.unlink(text)
    return decoder[0].data.decode()
    