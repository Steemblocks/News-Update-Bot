# Discord News Bot - Setup Guide

## Required Configuration

Your bot is running, but needs 2 things to work:

### 1. Update config.json with Your Discord Channel ID

Edit `config.json` and replace:
```json
"channel_id": "your_channel_id_here"
```

With your actual Discord channel ID.

#### How to get your Channel ID:

1. **Enable Developer Mode in Discord**
   - Open Discord Settings
   - Go to: Settings → Advanced → Developer Mode (toggle ON)

2. **Get the Channel ID**
   - Right-click on the channel where you want news posted
   - Select "Copy Channel ID"
   - Paste it in config.json

3. **Example:**
```json
"channel_id": "1234567890123456789"
```

### 2. Verify Bot Permissions

Make sure your bot has these permissions in the channel:
- ✅ Send Messages
- ✅ Embed Links
- ✅ Read Messages
- ✅ View Channel

#### To set permissions:
1. Go to Server Settings → Roles
2. Find your bot's role
3. Enable "Send Messages" and "Embed Links"

---

## Current Status

✅ Bot is running with token configured  
⚠️ Waiting for channel_id configuration  

Once you update `config.json` with your channel ID, the bot will:
- Check for new articles every 2 minutes
- Auto-post to your Discord channel
- Use commands: `!news`, `!bothelp`

---

## Bot Commands

| Command | Description |
|---------|-------------|
| `!news usa` | Get USA news |
| `!news uk` | Get UK news |
| `!news europe` | Get European news |
| `!news all` | Get all news |
| `!bothelp` | Show help |

---

## Troubleshooting

**Bot not posting articles?**
- Check channel_id in config.json
- Verify bot has "Send Messages" permission
- Check bot is in the correct Discord server
- Wait 2 minutes for next check cycle

**Bot not connecting?**
- Verify token in config.json is correct
- Check internet connection
- Try restarting the bot

**Still not working?**
- Check terminal for error messages
- Verify config.json syntax is valid JSON
- Make sure channel_id is a valid number

---

## Next Steps

1. Copy your channel ID
2. Update config.json
3. Save the file
4. Bot will start posting in 2 minutes

Happy news tracking! 🎉
