import logging
import os
from typing import List, Text
import qr
import read
from telegram import Update, update
from telegram.ext import *

# Configurar el Login
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ESTADOS DE LA CONVERSACION
GETNAME = 0
GETIMG = 0

# VARIABLES GLOBALES
name = []
name_dictionary = {}

# COMANDOS NORMALES DEL BOT
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.chat_id
    user_name = update.effective_user
    logger.info(f'Users: {user_name.first_name} is starting')

    context.bot.sendMessage(
        chat_id=user, 
        parse_mode="MarkdownV2",
        text="👋🏻👋🏻👋🏻 Hola❕, con este bot podras crear tu propio codigo *QR*, incluso leer cualquier otro\n\n"
             "Aqui tienes una _lista de los comandos_ a usar\n"
             "1️⃣ Enviar texto para convertir a *QR*: /to\_qr\n"
             "2️⃣ Enviar *QR* para leerlo: /to\_qr\n"
             "3️⃣ Para mas ayuda: /help\n"
            )
    

def help(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    logger.info(f'Users: {user.first_name} is asking for help')

    user = update.message.chat_id
    context.bot.sendMessage(
        chat_id=user, 
        parse_mode="MarkdownV2",
        text="Que es un codigo *QR*❓\n\n"
             "📌*Codigo QR:* Los códigos QR \(Quick Response\) son códigos de barras, capaces de almacenar determinado tipo de información, como una URL, SMS, EMail, Texto, etc\. Gracias al auge de los nuevos teléfonos inteligentes o SmarthPhone 📱 estos códigos QR están actualmente muy de moda 📈\n\n"
             "Este bot 🤖 es muy simple, solo tienes que segir los pasos cuando pulses aqui /to\_qr y tendras tu imagen 👌🏻, vamos❕❕ pulsa aqui /to\_qr ya❕❕\."
            )
    
# CONVERSACION PARA GENERAR CODIGO QR
def in_qr(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    logger.info(f'Users: {user.first_name} is on ConversationHandler as Generetor QR')

    update.message.reply_text(
        'Por favor, envie el texto que desea llevar a codigo QR\n'
        'Si desea cancelar, toque aqui /cancel'
    )
    return GETNAME

def get_name(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    logger.info(f'Users: {user.first_name} is making QR code')

    text = update.message.text   # Guardo el texto entrado
    chat_id = update.message.chat_id

    name = qr.generetor(text)    # Aplico la funcion generetor q retorna el nombre de la imagen del codigo 
    with open(name, "rb") as file:      # Abro la imagen en modo rb q es "lectura de binarios"
        context.bot.sendPhoto(chat_id=chat_id, photo=file)        # Envio la imagen al chat

    return ConversationHandler.END

# CONVERSACION PARA LEER CODIGO QR
def from_qr(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    logger.info(f"User: {user.first_name} convert from QR code")

    update.message.reply_text(
        'Por favor, envie la foto del QR que desea decodificar'
    )
    return GETIMG

def get_img(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    logger.info(f'Users: {user.first_name} is reading QR code')
    chat_id = update.message.chat_id
    name = update.message.message_id # Adquiero el id del mensaje enviado q es unico para cada uno (Evitando conflicto de nombres)
    name = str(name) + '.png'  # Paso el valor de name a str y le agrego el formato .png 

    # Descargando la imagen entrada
    file_id = update.message.photo[-1]   # Aquiero la ultima posicion de la lista de photo, para trabajar con tu valor
    new_file = context.bot.getFile(file_id)  # lo guardo en new_file
    new_file.download(name)  # lo descargo

    texto = read.read_qr(name)  # Aplico la funcion read q retorna la lectura del codigo

    context.bot.sendMessage(
        chat_id=chat_id,
        parse_mode="MarkdownV2",
        text=f"*Resultado de lectura de codigo*: _{texto}_"
        )
    return ConversationHandler.END

# COMANDO PARA CANCELAR CUALQUIERA DE LAS DOS CONVERSACIONES
def cancel(update: Update, context: CallbackContext)->None:
    user = update.effective_user
    logger.info(f'Users: {user.first_name}, cancel process')
    update.message.reply_text(
        'Se ha interrumpido el proceso de convercion.'
    )
    return ConversationHandler.END

# FUNCION PRINCIPAL DEL PROGRAMA
def main():
    # Solicitar TOKEN
    TOKEN = os.getenv("TOKEN")
    print(TOKEN)

    # Creo el Updater
    update = Updater(TOKEN)

    # Creo un dispatcher
    dp = update.dispatcher
    # CREAMOS CONVERSACION PARA GENERAR QR
    conv_handler_add = ConversationHandler(
        entry_points=[CommandHandler("to_qr", in_qr)],
        states ={
            GETNAME: [MessageHandler(Filters.text & ~Filters.command,  get_name)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    # CREAMOS CONVERSACION PARA LEER QR
    conv_handler_read = ConversationHandler(
        entry_points=[CommandHandler('from_qr', from_qr)],
        states={
            GETIMG:[MessageHandler(Filters.photo & ~Filters.command, get_img)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    # CREAMOS LOS MANEJADORES
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(conv_handler_add)
    dp.add_handler(conv_handler_read)

    # INICIAMOS NUESTRO BOT 
    update.start_polling()
    # PARA CERARLO CON CTRL+C
    update.idle()

if __name__=="__main__":
    main()