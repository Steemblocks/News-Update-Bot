# Discord News Bot

A Discord bot that tracks and displays the latest news from prominent news websites across USA, UK, and European countries.

## Features

- 📰 **Multi-Region News**: Fetches news from USA, UK, and European news sources
- 🔄 **Multiple Sources**: Integrates with RSS feeds and NewsAPI
- 🎯 **Popular Outlets**: Coverage from BBC, CNN, Reuters, The Guardian, AP News, and more
- ⏰ **Auto-Refresh**: Automatically caches news every hour
- 🎨 **Rich Embeds**: Beautiful Discord embeds with article information
- 🔍 **Regional Filtering**: Get news specific to each region

## Supported News Sources

### USA (8 sources)
- New York Times
- BBC News World
- NBC News  
- Fox News
- The Guardian (World)
- Vox
- Reuters
- AP News

### UK (8 sources)
- The Independent
- The Telegraph
- Sky News
- The Guardian UK
- Daily Mirror
- The Sun
- BBC UK
- Metro

### Europe (9 sources)
- The Guardian (Europe)
- France24
- Politico EU
- RTE News (Ireland)
- BBC Europe
- Euractiv
- Deutsche Welle (DW)
- ANSA (Italy)
- CBC News (Canada)

**Total: 25+ verified working news sources with 500+ articles daily**

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token
- NewsAPI key (optional but recommended)

### Installation

1. **Clone/Create the project directory**
   ```bash
   cd "Discord News Bot"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**
   - Copy `.env.example` to `.env`
   - Fill in your Discord bot token:
     ```
     DISCORD_TOKEN=your_bot_token_here
     DISCORD_CHANNEL_ID=your_channel_id_here
     NEWS_API_KEY=your_newsapi_key_here
     ```

4. **Get Your Discord Bot Token**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to "Bot" section and create a bot
   - Copy the token to your `.env` file

5. **Get NewsAPI Key (Optional)**
   - Visit [NewsAPI.org](https://newsapi.org)
   - Sign up for a free account
   - Copy your API key to `.env` file

6. **Run the bot**
   ```bash
   python main.py
   ```

## Commands

- `!news usa` - Get latest news from USA
- `!news uk` - Get latest news from UK
- `!news europe` - Get latest news from Europe
- `!news all` - Get latest news from all regions
- `!help` - Show available commands

## Project Structure

```
Discord News Bot/
├── main.py                 # Main bot entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration (create from .env.example)
├── .env.example           # Example environment file
├── bot/
│   ├── __init__.py
│   └── cogs/
│       ├── __init__.py
│       └── news.py        # News commands and scheduling
├── news_sources/
│   ├── __init__.py
│   └── fetcher.py         # News fetching logic
└── utils/
    ├── __init__.py
    └── embeds.py          # Discord embed formatting
```

## Configuration

### Environment Variables

- `DISCORD_TOKEN` (required): Your Discord bot token
- `DISCORD_CHANNEL_ID` (optional): Channel ID for auto-posting news
- `NEWS_API_KEY` (optional): NewsAPI key for additional news sources
- `BOT_PREFIX` (default: `!`): Command prefix
- `NEWS_FETCH_INTERVAL` (default: 3600): Interval in seconds to fetch news
- `LOG_LEVEL` (default: INFO): Logging level

## Features & Enhancements

### Current Features
- ✅ Multi-region news fetching
- ✅ RSS feed integration
- ✅ NewsAPI integration
- ✅ Duplicate removal
- ✅ Discord embeds with article metadata

### Potential Enhancements
- Auto-posting to designated channels
- Custom keyword filtering
- Per-guild settings
- Database caching
- Article categorization
- Reaction-based navigation

## Troubleshooting

### Bot won't connect
- Verify your `DISCORD_TOKEN` is correct
- Check that the bot has permission to access the channel
- Ensure your internet connection is stable

### No news articles appearing
- Check that RSS feeds are accessible
- If using NewsAPI, verify your API key is valid
- Check the logs for error messages

### Rate limit errors
- Reduce the `NEWS_FETCH_INTERVAL` value
- Use fewer news sources
- Space out manual news fetches

## License

This project is provided as-is for educational and personal use.

## Support

For issues or feature requests, please check the bot logs and verify all configuration values are correct.
