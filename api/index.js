export default async function handler(req, res) {
  if (req.method === "GET") {
    return res.status(200).send("Trader Naaz Telegram Bot is LIVE on Vercel 24/7!");
  }

  if (req.method === "POST") {
    try {
      const update = req.body || {};
      const BOT_TOKEN = "8987546183:AAGtzt1AMMsnTl_XUMMjEpG_PHDQgzfVzcs";
      const ADMIN_USERNAME = "@Naaz_Khan78";
      const SIGNUP_LINK = "https://broker-qx.pro/sign-up/?lid=1143940";
      const WELCOME_MESSAGE = `🚀 JOIN TRADER NAAZ VIP COMPOUNDING GROUP! 🚀\n\nReady to take your trading journey seriously? Our target is to grow $100 to $1,000 through disciplined entries, proper risk management, and step-by-step compounding sessions. 📈🔥\n\n✅ VIP Trading Signals\n✅ Live Compounding Sessions\n✅ Proper Money Management\n✅ Step-by-Step Guidance\n✅ Limited Members Only\n\nDon't miss the next session—create your account, deposit your trading capital, and join the TRADER NAAZ VIP FAMILY today!\n\n🔗 Join Link: ${SIGNUP_LINK}\n\n📩 Contact Admin: ${ADMIN_USERNAME}`;

      const joinRequest = update.chat_join_request;
      if (joinRequest) {
        const user = joinRequest.from || {};
        const chat = joinRequest.chat || {};
        const userId = user.id;
        const userChatId = joinRequest.user_chat_id || userId;
        const chatId = chat.id;

        // Step 1: Send Welcome DM FIRST (before approving)
        if (userChatId) {
          try {
            await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                chat_id: userChatId,
                text: WELCOME_MESSAGE,
                disable_web_page_preview: false,
              }),
            });
          } catch (e) {
            console.error("Error sending DM:", e);
          }
        }

        // Step 2: Approve Join Request
        if (chatId && userId) {
          try {
            await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/approveChatJoinRequest`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                chat_id: chatId,
                user_id: userId,
              }),
            });
          } catch (e) {
            console.error("Error approving request:", e);
          }
        }
      }

      // Handle /start in private chat
      const message = update.message;
      if (message && message.text && message.text.startsWith("/start") && message.chat?.type === "private") {
        await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_id: message.chat.id,
            text: WELCOME_MESSAGE,
            disable_web_page_preview: false,
          }),
        });
      }
    } catch (err) {
      console.error("Webhook processing error:", err);
    }
    return res.status(200).json({ ok: true });
  }

  return res.status(200).send("OK");
}
