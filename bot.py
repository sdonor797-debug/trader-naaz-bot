import asyncio
import logging
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ChatJoinRequestHandler, ContextTypes

# ─── Load environment variables ───────────────────────────────────────────────
load_dotenv(override=False)
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "@Naaz_Khan78")
SIGNUP_LINK = os.getenv("SIGNUP_LINK", "https://broker-qx.pro/sign-up/?lid=1143940")

# ─── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─── Health Check HTTP Server (for Render.com free web service) ───────────────
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OK - Trader Naaz Join Bot is Active\n")

    def log_message(self, format, *args):
        pass  # suppress access log spam

def start_health_server() -> None:
    port = int(os.getenv("PORT", 8080))
    try:
        server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
        logger.info(f"🌐 Health check HTTP server listening on port {port}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"❌ Could not start health check server: {e}")


# ─── Welcome message ──────────────────────────────────────────────────────────
DEFAULT_WELCOME_MESSAGE = f"""🚀 JOIN TRADER NAAZ VIP COMPOUNDING GROUP! 🚀

Ready to take your trading journey seriously? Our target is to grow $100 to $1,000 through disciplined entries, proper risk management, and step-by-step compounding sessions. 📈🔥

✅ VIP Trading Signals
✅ Live Compounding Sessions
✅ Proper Money Management
✅ Step-by-Step Guidance
✅ Limited Members Only

Don't miss the next session—create your account, deposit your trading capital, and join the TRADER NAAZ VIP FAMILY today!

🔗 Join Link: {SIGNUP_LINK}

📩 Contact Admin: {ADMIN_USERNAME}"""

WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", DEFAULT_WELCOME_MESSAGE)


# ─── Handler: /start Command ──────────────────────────────────────────────────
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when user sends /start."""
    if update.effective_user:
        await update.message.reply_text(WELCOME_MESSAGE, disable_web_page_preview=False)


# ─── Handler: Chat Join Request ───────────────────────────────────────────────
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Auto-approve channel join request and send a welcome DM."""
    join_request = update.chat_join_request
    if not join_request:
        return

    user = join_request.from_user
    chat = join_request.chat

    logger.info(
        f"New join request — User: {user.full_name} (@{user.username}) | "
        f"ID: {user.id} | Channel: {chat.title}"
    )

    # ── Step 1: Send welcome DM using user_chat_id (BEFORE approving) ───────────
    # Telegram allows bots to message users via user_chat_id during a join request.
    # We must send this BEFORE approving, while Telegram's temporary conversation window is active.
    target_chat_id = getattr(join_request, "user_chat_id", None) or user.id
    try:
        await context.bot.send_message(
            chat_id=target_chat_id,
            text=WELCOME_MESSAGE,
            disable_web_page_preview=False,
        )
        logger.info(f"📩 Welcome message delivered to: {user.full_name} (chat_id: {target_chat_id})")
    except Exception as e:
        logger.warning(
            f"⚠️ Could not send welcome DM to {user.full_name} (chat_id: {target_chat_id}): {e}"
        )

    # ── Step 2: Approve the join request ──────────────────────────────────────
    try:
        await join_request.approve()
        logger.info(f"✅ Approved join request: {user.full_name} (ID: {user.id})")
    except Exception as e:
        err_msg = str(e).lower()
        if "hide_requester_missing" in err_msg or "already" in err_msg:
            logger.info(f"ℹ️ Join request was already handled/approved for {user.full_name} (ID: {user.id})")
        else:
            logger.error(f"❌ Error approving join request for {user.full_name} (ID: {user.id}): {e}")

    # Small pause to avoid Telegram flood rate limits
    await asyncio.sleep(0.3)


# ─── Main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.critical("❌ BOT_TOKEN is missing or not set! Please edit your .env file.")
        raise SystemExit(1)

    logger.info("🤖 Starting TRADER NAAZ Join Bot...")

    app = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(ChatJoinRequestHandler(handle_join_request))

    # Start health check server in background thread (required for Render web services)
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()

    logger.info("✅ Bot is running. Listening for join requests... (Press Ctrl+C to stop)")
    app.run_polling(allowed_updates=["chat_join_request", "message"])


if __name__ == "__main__":
    main()
