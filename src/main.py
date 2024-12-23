from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from bot import TelegramBot
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    # Initialize the bot with your token
    bot_token = 'YOUR_BOT_TOKEN'
    application = Application.builder().token(bot_token).build()

    # Create an instance of the TelegramBot class
    telegram_bot = TelegramBot()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", telegram_bot.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_bot.handle_message))

    # Log that the bot has started
    logger.info("Bot started")

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()