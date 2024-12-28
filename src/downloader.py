import yt_dlp
import logging
import os
import re

# Initialize logger
logger = logging.getLogger(__name__)

def download_video_with_audio(url, quality, title):
    format_mapping = {
        "144p": "160",
        "240p": "133",
        "360p": "134",
        "480p": "135",
        "720p": "136",
        "1080p": "137",
        "audio": "140",
        "best": "bestvideo+bestaudio",
        "mp3": "bestaudio"
    }
    
    video_format = format_mapping.get(quality, "best")
    sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", title)
    if quality == "mp3":
        ydl_opts = {
            'format': video_format,
            'outtmpl': f'media/{sanitized_title}_{quality}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        if '+' not in video_format:
            format_code = f"{video_format}+140"  # Merge video format with audio (140 is m4a audio format)
        else:
            format_code = video_format

        ydl_opts = {
            'format': format_code,
            'merge_output_format': 'mp4',  # Output as a single MP4 file
            'outtmpl': f'media/{sanitized_title}_{quality}.%(ext)s',  # File naming convention with media directory
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            logger.info(f"Downloaded {quality} successfully.")
            return f"Downloaded {sanitized_title}_{quality}.mp4 successfully."
        except yt_dlp.utils.DownloadError as e:
            logger.error(f"Error: {e}")
            return f"An error occurred during download: {e}"

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
                "1080p": "137", "1440p": "308", "2160p": "315", "audio": "140", "mp3": "mp3", "best": "bestvideo+bestaudio"
            }
            reverse_mapping = {v: k for k, v in format_mapping.items()}
            allowed_qualities = {"144p", "240p", "360p", "480p", "720p", "1080p", "2160p"}
            qualities = list(set(reverse_mapping.get(f['format_id'], f.get('format_note', 'Unknown')) for f in formats if 'format_id' in f and 'vcodec' in f and f['vcodec'] != 'none' and reverse_mapping.get(f['format_id'], f.get('format_note', 'Unknown')) in allowed_qualities))
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
        title = self.get_video_title()
        return download_video_with_audio(self.url, quality, title)
