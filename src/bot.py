from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from downloader import VideoDownloader
import logging

# Initialize logger
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        pass

    def start_bot(self, token):
        application = Application.builder().token(token).build()
        start_handler = CommandHandler('start', self.start)
        application.add_handler(start_handler)
        message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        application.add_handler(message_handler)
        application.add_handler(CallbackQueryHandler(self.handle_quality_selection))
        application.run_polling()

    async def start(self, update: Update, context: CallbackContext):
        await update.message.reply_text('Hello! Send me a YouTube link to download the video.')

    async def handle_message(self, update: Update, context: CallbackContext):
        try:
            user_message = update.message.text
            logger.info(f"Received message: {user_message}")
            downloader = VideoDownloader(user_message)
            qualities = downloader.get_video_quality()
            thumbnail = downloader.get_video_thumbnail()
            title = downloader.get_video_title()
            
            if qualities:
                logger.info(f"Available qualities: {qualities}")
                if 'mp3' not in qualities:
                    qualities.append('mp3')  # Ensure MP3 option is included
                qualities = sorted(qualities, key=lambda x: (x != 'mp3', x))  # Sort qualities in ascending order, with MP3 at the end
                keyboard = [[InlineKeyboardButton(q if q != 'mp3' else 'MP3', callback_data=f"{user_message}|{q}") for q in qualities]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_photo(photo=thumbnail, caption=f"Title: {title}\nPlease select the video quality:", reply_markup=reply_markup)
                context.user_data['video_url'] = user_message  # Store the video URL in user data
            else:
                logger.warning(f"Invalid YouTube link: {user_message}")
                await update.message.reply_text('Invalid YouTube link. Please send a valid link.')
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def handle_quality_selection(self, update: Update, context: CallbackContext):
        try:
            query = update.callback_query
            await query.answer()
            data = query.data.split('|')
            quality = data[1]
            url = data[0]  # Retrieve the video URL from the callback data
            logger.info(f"Selected quality: {quality} for URL: {url}")
            downloader = VideoDownloader(url)
            result = downloader.download_video(quality)
            await query.edit_message_text(text=result)
        except Exception as e:
            logger.error(f"An error occurred: {e}")