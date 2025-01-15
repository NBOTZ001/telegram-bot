from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from bot import TelegramBot
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    # Initialize the bot with your token
    bot_token = '6131505585:AAE3n8lbHeC0JZ8L954ZFEyjvch9Ey8Q2VY'
    application = Application.builder().token(bot_token).build()

    # Create an instance of the TelegramBot class
    telegram_bot = TelegramBot()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", telegram_bot.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_bot.handle_message))
    application.add_handler(CallbackQueryHandler(telegram_bot.handle_quality_selection))

    # Log that the bot has started
    logger.info("Bot started")

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
