from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import telegram.error  # Import the telegram.error module
from downloader import VideoDownloader
import logging
import os

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
                keyboard = []
                for i in range(0, len(qualities), 2):
                    row = [InlineKeyboardButton(qualities[j] if qualities[j] != 'mp3' else 'MP3', callback_data=f"{user_message}|{qualities[j]}") for j in range(i, min(i + 2, len(qualities)))]
                    keyboard.append(row)
                reply_markup = InlineKeyboardMarkup(keyboard)
                qualities_str = ', '.join(qualities)
                await update.message.reply_photo(photo=thumbnail, caption=f"Title: {title}\nAvailable qualities: {qualities_str}\nPlease select the video quality:", reply_markup=reply_markup)
                context.user_data['video_url'] = user_message  # Store the video URL in user data
            else:
                logger.warning(f"Invalid YouTube link: {user_message}")
                await update.message.reply_text('Invalid YouTube link. Please send a valid link.')
        except Exception as e:
            logger.error(f"An error occurred while handling the message: {e}")
            await update.message.reply_text('An error occurred while processing your request.')

    async def handle_quality_selection(self, update: Update, context: CallbackContext):
        try:
            query = update.callback_query
            await query.answer()
            logger.info(f"Callback query data: {query.data}")
            data = query.data.split('|')
            if len(data) != 2:
                raise ValueError("Button_data_invalid")
            quality = data[1]
            url = data[0]  # Retrieve the video URL from the callback data
            logger.info(f"Selected quality: {quality} for URL: {url}")
            downloader = VideoDownloader(url)
            available_qualities = downloader.get_video_quality()
            if quality not in available_qualities:
                result = f"Requested format {quality} is not available. Please select a different quality."
                if query.message.text:
                    await query.edit_message_text(text=result)
                else:
                    await query.message.reply_text(text=result)
                return
            result = downloader.download_video(quality)
            if "Downloaded video" in result:
                sanitized_title = downloader.sanitize_title(downloader.get_video_title())
                video_path = os.path.join(os.getcwd(), 'media', f"{sanitized_title}.mp4")
                await query.message.reply_video(video=open(video_path, 'rb'), caption=result)
            else:
                if query.message.text:
                    await query.edit_message_text(text=result)
                else:
                    await query.message.reply_text(text=result)
        except ValueError as ve:
            logger.error(f"An error occurred: {ve}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            try:
                if query.message.text:
                    await query.edit_message_text(text="An error occurred during download.")
                else:
                    await query.message.reply_text(text="An error occurred during download.")
            except telegram.error.BadRequest as br:
                logger.error(f"An error occurred while editing the message: {br}")
                await query.message.reply_text("An error occurred during download.")