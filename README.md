# Telegram YouTube Bot

This bot allows users to download YouTube videos in various qualities directly from Telegram.

## Features
- Download videos in different qualities (144p, 240p, 360p, 480p, 720p, 1080p)
- Download audio as MP3
- Get video information such as title and thumbnail

## Project Structure

```
telegram-bot
├── src
│   ├── main.py          # Entry point of the application
│   ├── bot.py           # Contains the TelegramBot class for managing bot interactions
│   ├── downloader.py     # Contains the VideoDownloader class for downloading videos
│   └── utils
│       └── __init__.py  # Utility functions and constants
├── requirements.txt      # Lists project dependencies
└── README.md             # Documentation for the project
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/STARK-404/telegram-youtube-bot.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python src/main.py
   ```

## Usage Guidelines

1. Start the bot by sending the `/start` command.
2. Send a YouTube link to the bot.
3. Select the desired video quality from the provided options.
4. The bot will download the video and send it to you.

## Owner
This project is owned and maintained by [STARK-404](https://github.com/STARK-404).

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.
