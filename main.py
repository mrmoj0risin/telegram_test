import logging
import requests
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(f'Help! 1234')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(f'Вы написали:   {update.message.text}')
    print(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def calc(update, context):
    x = re.findall(r'/(\d+)([+,-,\/,*])(\d+)', update.message.text)
    update.message.reply_text(f'{x}          RES')
    print(x)


"""

Here we get a random picture of dog and return it

"""

def get_url_dog():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url_dog():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url_dog()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
        return url


def get_dog(update, context):
    url = get_image_url_dog()
    update.message.reply_text(url)


"""

same with cats

"""

def get_url_cat():
    contents = requests.get('https://api.thecatapi.com/v1/images/search').json()
    # print(contents[0]["url"])
    url = contents[0]["url"]
    return url

def get_image_url_cat():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url_cat()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
        return url

def get_cat(update,context):
    url = get_url_cat()
    update.message.reply_text(url)


def main():


    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1619816230:AAGotxrcOEnj-n-HCplQ659QzDo8SD9e7OI", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('dog', get_dog))
    dp.add_handler(CommandHandler("cat", get_cat))
    dp.add_handler(CommandHandler("calc", calc))


    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
