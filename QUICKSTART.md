# QUICK START GUIDE

## Installation (3 Easy Steps)

### Step 1: Install Dependencies
```bash
pip3 install --break-system-packages python-telegram-bot==20.7 python-dotenv==1.0.0
```

**If that doesn't work, try:**
```bash
pip3 install --user python-telegram-bot==20.7 python-dotenv==1.0.0
```

### Step 2: Get Your Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 3: Configure and Run

**Option A: Using .env file (Recommended)**
```bash
# Copy the example file
cp .env.example .env

# Edit it and add your token
nano .env
# Change: TELEGRAM_BOT_TOKEN=your_bot_token_here
# To: TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Run the bot
python3 telegram_video_bot_enhanced.py
```

**Option B: Using environment variable**
```bash
export TELEGRAM_BOT_TOKEN='123456789:ABCdefGHIjklMNOpqrsTUVwxyz'
python3 telegram_video_bot.py
```

### Step 4: Add Bot to Your Group

1. Add the bot to your Telegram group
2. Make it an **admin** (must have permission to read messages)
3. Send a video to test!

---

## Automated Installation

Run this for automatic setup:
```bash
chmod +x install.sh
./install.sh
```

---

## Testing the Bot

Once running, test it:
1. Send `/start` in your group
2. Send a video (any length)
3. The bot will check if it's 2+ hours

---

## Common Issues

**"pip3: command not found"**
- Use `pip3` instead of `pip`
- Or install: `sudo apt install python3-pip`

**"Permission denied"**
- Try: `pip3 install --user <package>`
- Or: `pip3 install --break-system-packages <package>`

**Bot doesn't respond**
- Make sure bot is admin in the group
- Check the bot token is correct
- Look for errors in the terminal

---

## Need Help?

See the full **README.md** for detailed documentation!
