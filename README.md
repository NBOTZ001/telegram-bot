# Telegram Video Downloader Bot

This project is a Telegram bot that allows users to download videos from YouTube. When a user sends a YouTube link, the bot prompts them to select the desired video quality before downloading.

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

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd telegram-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Telegram bot by talking to [BotFather](https://t.me/botfather) and obtain your bot token.

4. Update the bot token in `src/main.py`.

## Usage Guidelines

1. Run the bot:
   ```
   python src/main.py
   ```

2. Send a YouTube link to the bot.

3. Select the desired video quality from the options provided.

4. The bot will download the video and send it back to you.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.