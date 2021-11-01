import logging
from uuid import uuid4
import os

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, CallbackQueryHandler
from telegram.utils.helpers import escape_markdown

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query == "":
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Primer Teclado",
            input_message_content=InputTextMessageContent("Primer teclado inline"),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Btn-1", url="https://core.telegram.org/bots/api"), InlineKeyboardButton(text="Btn-2", url="https://core.telegram.org/bots/api")],
                 [InlineKeyboardButton(text='Share', callback_data='share')]
                 ]
            ),
            thumb_url="https://www.pngwing.com/es/free-png-bhzqg",

            
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            ),
        ),
    ]

    update.inline_query.answer(results)

def share(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    chat_id = update.message.chat_id
    print(query.copy_message(chat_id=chat_id))

def main() -> None:
    """Run the bot."""
    # Get the API_TOKEN
    TOKEN = os.getenv("TOKEN")
    # Create the Updater and pass it your bot's token.
    updater = Updater("2021964034:AAEYeCjmU54O00eUTXNlEgh-soy1rWvO54M")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CallbackQueryHandler(pattern='share', callback=share))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    
    updater.start_webhook(
        listen='0.0.0.0', 
        port=PORT, 
        url_path=TOKEN, 
        webhook_url=f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}')

    updater.idle()


if __name__ == '__main__':
    main()