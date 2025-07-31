from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from flask import Flask, request, jsonify
from telegram import Bot
# --- BOT SETTINGS ---
TOKEN = '8467430850:AAFO_GWzXxNct40AxIdNIoPFY7p9E83i4fw'  # 🔐 BotFather থেকে নতুন token নিন
CHANNEL_ID = -1002833876047   # ✅ আপনার প্রাইভেট চ্যানেল/গ্রুপ আইডি
CHANNEL_ID2 = -1002808301387
WEBAPP_URL = "https://diamzonestore.in/ads/"  # 💻 আপনার ওয়েব অ্যাড পেইজ

# --- /start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            # ✅ Notify in your admin group/channel
            await context.bot.send_message(
                chat_id=CHANNEL_ID2,
                text=f"👤 New user joined: [{update.effective_user.first_name}](tg://user?id={user_id})",
                parse_mode="Markdown"
            )

            # ✅ Show welcome animation + mini app button
            gif_url = "https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyYnJ4Z242bTdodWoyZjQwM3k4YmUyc2dzMTl1dDFkZGZtNnE1bmRmbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YTRUPHI7fXK6s/giphy.gif"
            await context.bot.send_animation(
                chat_id=user_id,
                animation=gif_url,
                caption=(
                    "🎉 Welcome to Easy Earning Bot!\n\n"
                    "💸 Earn real rewards by watching ads on our Telegram Bot.\n"
                    "🔥 It's simple: view ads, earn money, and withdraw anytime.\n\n"
                    "👉 Tap the button below to start earning now!"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚀 Start Earning", web_app=WebAppInfo(url=WEBAPP_URL))]
                ])
            )
        else:
            raise Exception("User not joined")
    except:
        # ❌ User not in channel
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "🔒 To use this bot, you must join our private channel first.\n\n"
                "📢 Please join the channel using the button below, then click ✅ I Joined."
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url="https://t.me/+6Wg_IQEplk4zODM1")],
                [InlineKeyboardButton("✅ I Joined", callback_data="check_join")]
            ])
        )

# --- Callback: ✅ I Joined ---
async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

# --- Main App Setup ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join_callback, pattern="check_join"))
    app.run_polling()
