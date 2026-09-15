# TRADER NAAZ — Telegram Join Request Bot

A Telegram bot that **automatically approves** private channel join requests and instantly sends a **welcome direct message (DM)** to every new member.

---

## ⚙️ Setup Guide (Quick & Easy)

### Step 1 — Create Bot with @BotFather
1. Open Telegram and search for [`@BotFather`](https://t.me/botfather).
2. Send `/newbot`.
3. Give it a name (e.g. `Trader Naaz Join Bot`) and a username ending in `bot` (e.g. `TraderNaazJoinBot`).
4. Copy the **HTTP API token** provided by BotFather.

### Step 2 — Configure the Token
1. Open the [`.env`](.env) file inside `trader-naaz-bot`:
   ```env
   BOT_TOKEN=your_actual_bot_token_here
   ADMIN_USERNAME=@tradernaaz
   SIGNUP_LINK=https://equlix.com/en/signup?lid=2945201
   ```
2. Replace `your_actual_bot_token_here` with the token copied from BotFather.
3. You can also customize `ADMIN_USERNAME` and `SIGNUP_LINK` if needed.

---

### Step 3 — Channel Settings
1. Open your Telegram Channel → **Edit** → **Channel Type**.
2. Make sure it is set to **Private**.
3. Under **Invite Links**, create or edit a link and turn ON **"Request Admin Approval"** (Approve new members).

### Step 4 — Add Bot as Channel Admin
1. Open your channel → **Administrators** → **Add Admin**.
2. Search for your bot username.
3. Enable the **"Invite Users via Link"** permission (or "Manage Join Requests").
4. Save.

---

## 🚀 Running the Bot Locally

### Install Dependencies
```bash
cd trader-naaz-bot
pip install -r requirements.txt
```

### Start the Bot
```bash
python3 bot.py
```

You should see:
```text
🤖 Starting TRADER NAAZ Join Bot...
✅ Bot is running. Listening for join requests... (Press Ctrl+C to stop)
```

---

## 🧪 Testing the Bot
1. Generate an invite link with **Request Admin Approval** turned on.
2. From another Telegram account, click the link and tap **Request to Join**.
3. The bot will:
   - ✅ Approve the request immediately.
   - 📩 Deliver the Trader Naaz VIP welcome message to the user's DMs.

---

## ☁️ Deployment (Run 24/7)

### On VPS (Background Process)
```bash
# Using screen
screen -S naaz-bot
python3 bot.py
# Press Ctrl+A then D to detach

# Or using pm2
pm2 start bot.py --name "trader-naaz-bot" --interpreter python3
```

### On Railway / Render / Heroku
The included `Procfile` allows 1-click worker deployment on Railway, Render, or Heroku:
```text
worker: python3 bot.py
```
Just set `BOT_TOKEN` in the platform's Environment Variables dashboard.
