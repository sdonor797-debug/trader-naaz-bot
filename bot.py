import logging
import os
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

    # ── Step 1: Approve the join request ──────────────────────────────────────
    approved = False
    try:
        await join_request.approve()
        approved = True
        logger.info(f"✅ Approved join request: {user.full_name} (ID: {user.id})")
    except Exception as e:
        logger.error(f"❌ Error approving join request for {user.full_name} (ID: {user.id}): {e}")

    # ── Step 2: Send welcome DM to the user ───────────────────────────────────
    if approved:
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text=WELCOME_MESSAGE,
                disable_web_page_preview=False,
            )
            logger.info(f"📩 Welcome message delivered to: {user.full_name} (ID: {user.id})")
        except Exception as e:
            logger.warning(
                f"⚠️ Could not send welcome DM to {user.full_name} (ID: {user.id}): {e}"
            )


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

    logger.info("✅ Bot is running. Listening for join requests... (Press Ctrl+C to stop)")
    app.run_polling(allowed_updates=["chat_join_request", "message"])


if __name__ == "__main__":
    main()
