import logging
import os
from typing import List, Text

from telegram.message import Message

from qr import generetor, send

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import *

# Configurar el Login
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ESTADOS DE LA CONVERSACION
MENU, GETOPTION, TOTEXT, GETTEXT, GETURL = range(5)

# Teclado
reply_keyboard = [
        ['QR: TEXTO','QR: URL'],
        ['AYUDA💡']
]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Seleccione el tipo de QR')


# COMANDOS NORMALES DEL BOT
def help(update: Update, context: CallbackContext):
    user = update.effective_user
    logger.info(f'Users: {user.first_name} is asking for help')
    user = update.message.chat_id
    update.message.reply_text(
        text="Qué es un codigo QR❓\n\n"
             "📌Codigo QR: Los códigos QR (Quick Response) son códigos de barras, capaces de almacenar determinado tipo de información, como una URL, SMS, EMail, Texto, etc. Gracias al auge de los nuevos teléfonos inteligentes o SmarthPhone 📱 estos códigos QR están actualmente muy de moda 📉\n\n"
             "Con este bot puede crear QRs de 2 tipos (URL, TEXT)",
             reply_markup=ReplyKeyboardMarkup([
                    ['Volver al Menu↩️']
                                               ], resize_keyboard=True)
            )

def to_qr(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Con este Bot podrá crear códigos QR',
        reply_markup=markup
    )
    return GETOPTION

def qr_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Envie el texto que desee...'
    )
    return GETTEXT

def qr_text_convert(update: Update, context: CallbackContext):

    text = update.message.text
    name_file = update.message.message_id
    file = generetor(text, name_file)
    chat = update.message.chat
    send(file, chat)
    update.message.reply_text(
        text = 'QR LISTO!!',
        reply_markup=ReplyKeyboardMarkup([['Volver al Menu↩️']], resize_keyboard=True)
    )
    return GETOPTION

def qr_url(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Envie el url que desee...'
    )
    return GETURL

def qr_url_convert(update: Update, context: CallbackContext):
    url = update.message.text
    name_file = update.message.message_id
    chat = update.message.chat
    file = generetor(url, name_file)
    send(file, chat)
    update.message.reply_text(
        text = 'QR LISTO!!',
        reply_markup=ReplyKeyboardMarkup([['Volver al Menu↩️']], resize_keyboard=True)
    )
    return GETOPTION



# FUNCION PRINCIPAL DEL PROGRAMA
def main():
    # Solicitar TOKEN
    TOKEN = os.getenv("TOKEN")
    print(TOKEN)

    # Creo el Updater
    update = Updater(TOKEN)

    # Creo un dispatcher
    dp = update.dispatcher
  
    # CREAMOS LOS MANEJADORES

    # Conversacion para crear QR
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', to_qr)],
        states={
            #MENU: [CommandHandler('stup', stup)],
            GETOPTION: [
                MessageHandler(Filters.regex('^QR: TEXTO$'), qr_text),
                MessageHandler(Filters.regex('^QR: URL$'), qr_url),
                MessageHandler(Filters.regex('^AYUDA💡$'), help),
                MessageHandler(Filters.regex('^Volver al Menu↩️$'), to_qr)
                ],
            MENU: [CommandHandler('menu', to_qr )],
            GETTEXT: [MessageHandler(Filters.text & ~Filters.command, qr_text_convert)],
            GETURL: [MessageHandler(Filters.entity('url'), qr_url_convert)]
        },
        fallbacks=[]
    )
    # Start the Bot
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    
    update.start_webhook(
        listen='0.0.0.0', 
        port=PORT, 
        url_path=TOKEN, 
        webhook_url=f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}')

    update.idle()
    
if __name__=="__main__":
    main()