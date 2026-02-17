# 🚂 Railway Deployment Guide

## Files You Need to Upload to GitHub

```
your-repo/
├── telegram_video_bot_final.py   ← main bot
├── requirements.txt               ← dependencies
├── Procfile                       ← tells Railway how to run
├── railway.json                   ← Railway config
├── runtime.txt                    ← Python version
└── .gitignore                     ← excludes secrets
```

---

## Step 1 — Create a GitHub Repository

1. Go to https://github.com → **New repository**
2. Name it (e.g. `video-monitor-bot`)
3. Set to **Private** (your token is in env vars but still safer)
4. Click **Create repository**

Upload these files:
- `telegram_video_bot_final.py`
- `requirements.txt`
- `Procfile`
- `railway.json`
- `runtime.txt`
- `.gitignore`

> ⚠️ Do NOT upload `.env`, `user_deficits.json`, or any `.json` data files

---

## Step 2 — Create Railway Project

1. Go to https://railway.app
2. Sign in with GitHub
3. Click **New Project**
4. Choose **Deploy from GitHub repo**
5. Select your repository
6. Railway will auto-detect Python ✅

---

## Step 3 — Set Environment Variables

In your Railway project dashboard:

1. Click your service
2. Go to **Variables** tab
3. Click **New Variable**
4. Add:

| Variable | Value |
|----------|-------|
| `TELEGRAM_BOT_TOKEN` | `your_token_from_botfather` |

> ⚠️ This is the ONLY variable needed. Never put the token in code.

---

## Step 4 — Add a Volume (Persistent Storage)

Railway's filesystem resets on redeploy. To keep bot data (streaks, deficits, hours) you need a volume:

1. In your project, click **New** → **Volume**
2. Mount path: `/app/data`
3. Then update the bot's data file paths to use `/app/data/`:

In `telegram_video_bot_final.py`, change the top constants:
```python
DATA_FILE = '/app/data/user_deficits.json'
TIMEZONE_FILE = '/app/data/group_timezone.json'
USER_TIMEZONES_FILE = '/app/data/user_timezones.json'
```
Also in `handle_video`, the video hashes file:
```python
HASH_FILE = '/app/data/video_hashes.json'
```

> Without a volume, data resets every time Railway redeploys your bot.

---

## Step 5 — Deploy

1. Railway auto-deploys when you push to GitHub
2. Go to **Deployments** tab to see logs
3. Look for: `🤖 Bot is starting...`

---

## Step 6 — Enable Reminders in Telegram

Once the bot is running:

1. Add the bot to your Telegram group as **admin**
2. Give it permissions: **Delete messages** + **Ban users**
3. In the group, type `/enablereminders`
4. Bot confirms with current time and schedule

---

## Checking Logs

In Railway dashboard:
- Click your service → **Deployments** → **View Logs**
- You'll see every video submission, deficit calculation, and scheduled message

---

## Keeping Bot Alive 24/7

Railway runs your bot continuously as a **worker** (not a web server).
- No sleep/idle issues like free Heroku
- Restarts automatically on crash (`restartPolicyMaxRetries: 10`)
- Runs 24/7 for ~$5/month on Hobby plan

---

## Common Issues

**Bot not responding?**
- Check logs in Railway dashboard
- Verify `TELEGRAM_BOT_TOKEN` is set correctly

**Data resetting on redeploy?**
- You haven't set up a Volume yet (Step 4)

**Scheduled messages not sending?**
- Run `/enablereminders` in the group
- Check timezone is set correctly with `/settimezone`

**Bot can't delete messages or kick users?**
- Make sure bot is admin with correct permissions in the group
