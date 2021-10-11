import logging
import os
from typing import List, Text

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, replymarkup
from telegram.ext import *
import rgqr
# Configurar el Login
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ESTADOS DE LA CONVERSACION
GETNAME = 0

# COMANDOS NORMALES DEL BOT
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.chat_id
    user_name = update.effective_user
    logger.info(f'Users: {user_name.first_name} is starting')
    
    update.message.reply_text(
        text="👋🏻👋🏻👋🏻 Hola❕, con este bot podras crear tu propio codigo QR, incluso leer cualquier otro\n\n Seleccione la opcion deseada",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Convertir a QR 🔁", callback_data="to_qr")],
            [InlineKeyboardButton(text="More Help 💡", callback_data="help")]
        ])
    )

def back(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(
        text="👋🏻👋🏻👋🏻 Hola❕, con este bot podras crear tu propio codigo QR, incluso leer cualquier otro\n\n Seleccione la opcion deseada",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Convertir a QR 🔁", callback_data="to_qr")],
            [InlineKeyboardButton(text="More Help 💡", callback_data="help")] 
        ])
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

def more_help(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(
           text="📌Codigo QR: Los códigos QR (Quick Response) son códigos de barras, capaces de almacenar determinado tipo de información, como una URL, SMS, EMail, Texto, etc. Gracias al auge de los nuevos teléfonos inteligentes o SmarthPhone 📱 estos códigos QR están actualmente muy de moda 📈\n\n"
                "Este bot 🤖 es muy simple, solo tienes que segir los pasos cuando pulses aqui /to_qr y tendras tu imagen 👌🏻, vamos❕❕ pulsa aqui /to_qr ya❕❕.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Back ↩️", callback_data="back")]   
        ])
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

def to_qr(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(
        text='Por favor, envie el texto que desea llevar a codigo QR\n Si desea cancelar, toque aqui /cancel'
    )
    return GETNAME

def get_name(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    chat = update.message.chat
    
    file = rgqr.generetor_qr(text)
    rgqr.send_file(file, chat)

    return ConversationHandler.END


# COMANDO PARA CANCELAR CONVERSACION
def cancel(update: Update, context: CallbackContext)->None:
    user = update.effective_user
    logger.info(f'Users: {user.first_name}, cancel process')
    update.message.reply_text(
        text='Se ha interrumpido el proceso de convercion.',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Convertir a QR 🔁", callback_data="to_qr")],
            [InlineKeyboardButton(text="More Help 💡", callback_data="help")] 
        ])
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
        entry_points=[
            CommandHandler("to_qr", in_qr),
            CallbackQueryHandler(pattern="to_qr", callback=to_qr)],
        states ={
            GETNAME: [MessageHandler(Filters.text & ~Filters.command,  get_name)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # CREAMOS LOS MANEJADORES
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(conv_handler_add)
    dp.add_handler(CallbackQueryHandler(pattern="help", callback=more_help))
    dp.add_handler(CallbackQueryHandler(pattern="back", callback=back))
    # INICIAMOS NUESTRO BOT 
    update.start_polling()
    # PARA CERARLO CON CTRL+C
    update.idle()

if __name__=="__main__":
    main()