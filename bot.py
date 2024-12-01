from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import time

# Token API - możesz ustawić go bezpośrednio tutaj
API_TOKEN = '7697064545:AAHWQCDqr5BYYqqmvU_Kc-Oah9aWb40k5rU'

# Lista chat_id subskrybentów
SUBSCRIBERS = []

# Funkcja startowa
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to FutureGreen Bot! 🌱\n"
        "Use /subscribe to receive updates about FGN and /menu to explore options!"
    )

# Funkcja do obsługi subskrypcji
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in SUBSCRIBERS:
        SUBSCRIBERS.append(chat_id)
        await update.message.reply_text("✅ You have successfully subscribed to FutureGreen updates!")
    else:
        await update.message.reply_text("You are already subscribed!")

# Funkcja FAQ
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faq_text = """
    🌿 **FutureGreen FAQ** 🌿
    1️⃣ **What is FGN?**
    FutureGreen (FGN) is a green cryptocurrency supporting sustainability.

    2️⃣ **How can I buy FGN?**
    FGN will be available on major DEX platforms soon.

    3️⃣ **How can I stay updated?**
    Use /subscribe to get updates from this bot!
    """
    await update.message.reply_text(faq_text, parse_mode="Markdown")

# Funkcja menu z przyciskami
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Visit Website", url="https://futuregreen.fun")],
        [InlineKeyboardButton("Join Telegram", url="https://t.me/FutureGreenFGN")],
        [InlineKeyboardButton("Follow on X", url="https://x.com/FutureGreenFGN")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌿 Choose an option:", reply_markup=reply_markup)

# Funkcja automatycznych powiadomień
async def send_post(context: ContextTypes.DEFAULT_TYPE):
    message = "🚀 Big news from FutureGreen! 🌱 Visit our website for updates: https://futuregreen.fun"
    for chat_id in SUBSCRIBERS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

# Główna funkcja
def main():
    # Tworzymy aplikację
    application = Application.builder().token(API_TOKEN).build()

    # Dodajemy obsługę komend
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("faq", faq))
    application.add_handler(CommandHandler("menu", menu))

    # Zadanie cykliczne: wiadomości co 12 godzin
    application.job_queue.run_repeating(send_post, interval=43200, first=10)

    # Uruchamiamy bota
    application.run_polling()

if __name__ == '__main__':
    main()
