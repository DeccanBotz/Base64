import os
import logging
from telegram import ChatAction,InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.utils.helpers import escape_markdown
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram.ext.dispatcher import run_async
from functools import wraps
from uuid import uuid4
import configparser as cfg
import base64

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN","")

OWNER = os.environ.get("OWNER", "")


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

@run_async     
@send_typing_action
def start(update, context):
    """Send a message when the command /start is issued."""
    global first
    first=update.message.chat.first_name
    keybord1 = [[InlineKeyboardButton("Tutorial 📽", url='https://youtu.be/GDqWA32N97o'),
                InlineKeyboardButton("Owner 👨‍💻", url=f'https://t.me/{OWNER}')]]
    reply_markup = InlineKeyboardMarkup(keybord1)
    update.message.reply_text('Hi! '+str(first)+' \n\nWelcome to Base 64 Bot.\n\nI can Encode & Decode a Text in Base 64, 32, 16.\n\nCheck /help for more...', reply_markup=reply_markup)

@run_async
@send_typing_action
def help(update, context):
    """Send a message when the command /help is issued."""
    global first
    first=update.message.chat.first_name
    keybord1 = [[InlineKeyboardButton("Tutorial 📽", url='https://youtu.be/GDqWA32N97o'),
                InlineKeyboardButton("Owner 👨‍💻", url=f'https://t.me/{OWNER}')]]
    reply_markup = InlineKeyboardMarkup(keybord1)
    update.message.reply_text('Hi! '+str(first)+' \n\nFollow these Steps...\n\nUse (/b64encode text) to encode into base 64 format\nUse (/b64decode text) to decode into base 64 format\nUse(/b32encode text) to encode into base 32 format\nUse (/b32decode text) to decode into base 32 format\nUse (/b16encode text) to encode into base 16 format\nUse (/b16decode text) to decode into base 16 format', reply_markup=reply_markup)


def b64encode_text(update, context):
    user_reply = update.message.text
    encoded_text = base64.urlsafe_b64encode(str.encode(user_reply.replace('/b64encode ','').strip()))
    update.message.reply_text(encoded_text.decode("utf-8"))

def b64decode_text(update, context):
    user_reply = update.message.text
    formatted_reply = user_reply.replace('/b64decode ','').strip()
    decoded_text = base64.urlsafe_b64decode(formatted_reply)
    update.message.reply_text(decoded_text.decode("utf-8"))

def b32encode_text(update, context):
    user_reply = update.message.text
    encoded_text = base64.b32encode(str.encode(user_reply.replace('/b32encode ','').strip()))
    update.message.reply_text(encoded_text.decode("utf-8"))

def b32decode_text(update, context):
    user_reply = update.message.text
    formatted_reply = user_reply.replace('/b32decode ','').strip()
    decoded_text = base64.b32decode(formatted_reply)
    update.message.reply_text(decoded_text.decode("utf-8"))

def b16encode_text(update, context):
    user_reply = update.message.text
    encoded_text = base64.b16encode(str.encode(user_reply.replace('/b16encode ','').strip()))
    update.message.reply_text(encoded_text.decode("utf-8"))

def b16decode_text(update, context):
    user_reply = update.message.text
    formatted_reply = user_reply.replace('/b16decode ','').strip()
    decoded_text = base64.b16decode(formatted_reply)
    update.message.reply_text(decoded_text.decode("utf-8"))


def main():
    token=TOKEN
    updater = Updater(token,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("b64encode", b64encode_text))
    dp.add_handler(CommandHandler("b64decode", b64decode_text))
    dp.add_handler(CommandHandler("b32encode", b32encode_text))
    dp.add_handler(CommandHandler("b32decode", b32decode_text))
    dp.add_handler(CommandHandler("b16encode", b16encode_text))
    dp.add_handler(CommandHandler("b16decode", b16decode_text))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
