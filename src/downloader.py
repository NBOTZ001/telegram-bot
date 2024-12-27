import yt_dlp
import logging
import os
import re

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
            format_mapping = {
                "144p": "160", "240p": "133", "360p": "134", "480p": "135", "720p": "136",
                "1080p": "299", "1440p": "308", "2160p": "315", "audio": "140", "mp3": "mp3", "best": "best"
            }
            reverse_mapping = {v: k for k, v in format_mapping.items()}
            qualities = list(set(reverse_mapping.get(f['format_id'], f.get('format_note', 'Unknown')) for f in formats if 'format_id' in f))
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

    def sanitize_title(self, title):
        return re.sub(r'[\\/*?:"<>|]', "_", title)

    def download_video(self, quality):
        download_path = os.path.join(os.getcwd(), 'media')
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        sanitized_title = self.sanitize_title(self.get_video_title())

        format_mapping = {
            "144p": "160", "240p": "133", "360p": "134", "480p": "135", "720p": "136",
            "1080p": "299", "1440p": "308", "2160p": "315", "audio": "140", "mp3": "mp3", "best": "best"
        }
        format_id = format_mapping.get(quality, quality)

        if quality == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'outtmpl': os.path.join(download_path, f'{sanitized_title}.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': format_id,
                'quiet': True,
                'outtmpl': os.path.join(download_path, f'{sanitized_title}.%(ext)s'),
            }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                logger.info(f"Downloaded video from URL: {self.url} at quality: {quality}")
                return f"Downloaded video at {quality} quality."
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return "An error occurred during download."