import yt_dlp
import logging
import os

# Initialize logger
logger = logging.getLogger(__name__)

class VideoDownloader:
    def __init__(self, url):
        self.url = url
        self.video_info = None

    def get_video_info(self):
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'simulate': True,
            'force_generic_extractor': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.video_info = ydl.extract_info(self.url, download=False)
                logger.info(f"Retrieved video info for URL: {self.url}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    def get_video_quality(self):
        if not self.video_info:
            self.get_video_info()
        if self.video_info:
            formats = self.video_info.get('formats', [])
            qualities = list(set(f['format_note'] for f in formats if 'format_note' in f))
            qualities.append('mp3')
            logger.info(f"Found qualities: {qualities} for URL: {self.url}")
            return qualities
        return None

    def get_video_thumbnail(self):
        if not self.video_info:
            self.get_video_info()
        if self.video_info:
            return self.video_info.get('thumbnail')
        return None

    def get_video_title(self):
        if not self.video_info:
            self.get_video_info()
        if self.video_info:
            return self.video_info.get('title')
        return None

    def download_video(self, quality):
        download_path = os.path.join(os.getcwd(), 'media')
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        if quality == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': f'best[format_note={quality}]',
                'quiet': True,
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                logger.info(f"Downloaded video from URL: {self.url} at quality: {quality}")
                return f"Downloaded video at {quality} quality."
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return "An error occurred during download."