import pyqrcode
from pyqrcode import QRCode
from telegram import ChatAction
from telegram.chat import Chat
import os

def generetor(content, name):
    name = str(name) + '.png'
    qrobj = pyqrcode.create(content)
    with open(name, 'wb') as f:
        file = qrobj.png(f, scale=10)
    return name

def send(name_file, chat: Chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_photo(
        photo=open(name_file, 'rb')
    )
    os.unlink(name_file)