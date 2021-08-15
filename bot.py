import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from bot_info import BOT_TOKEN

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

FIRST, SECOND = range(2)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user if they've watched."""
    reply_keyboard = [['Yes', 'Not Yet']]

    update.message.reply_text(
        """Hi! My name is PanConBot. I'm a JoJo lover. \n\n"""
        """Send /cancel to stop talking to me UwU.\n\n"""
        """Have you watched JoJo's?""",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder='Yes or Not Yet?'),
    )

    return FIRST


def watch(update: Update, context: CallbackContext) -> int:
    """Stores the selected watch response and asks if wants to watch."""
    reply_keyboard = [['Yes', 'Of course!']]

    user = update.message.from_user
    recieved_message = update.message.text
    logger.info("Has watched? of %s: %s", user.first_name, recieved_message)
    if recieved_message == 'Yes':
        reply_message = 'Awesome! Do you want to watch it again?'
    elif recieved_message == 'Not Yet':
        reply_message = """It's OK, Do you want to watch it?"""

    update.message.reply_text(reply_message,
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True,
                                  input_field_placeholder='Si?',
                              ))

    return SECOND


def info(update: Update, context: CallbackContext) -> int:
    """Gives info on where to watch."""

    user = update.message.from_user
    recieved_message = update.message.text
    logger.info("Will watch? of %s: %s", user.first_name, recieved_message)
    reply_message = """Great!

    You can watch parts 1-4 on:
    https://www.netflix.com/cl/title/80179831

    And part 5 on:
    https://www.crunchyroll.com/es/jojos-bizarre-adventure
    or just google it :v

    ENJOY!
    """
    update.message.reply_text(reply_message,
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [MessageHandler(Filters.regex('^(Yes|Not Yet)$'), watch)],
            SECOND:
            [MessageHandler(Filters.regex('^(Yes|Of course!)$'), info)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()