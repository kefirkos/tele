import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import time

# Token API
API_TOKEN = '7697064545:AAHWQCDqr5BYYqqmvU_Kc-Oah9aWb40k5rU'

# Listy subskrybentów i zapisanych na Airdrop
SUBSCRIBERS = []
airdrop_list = []

# Funkcje zapisu/odczytu Airdrop
def save_airdrop_list():
    """Zapisuje listę użytkowników zapisanych na Airdrop do pliku."""
    with open("airdrop_list.txt", "w") as file:
        for chat_id in airdrop_list:
            file.write(f"{chat_id}\n")

def load_airdrop_list():
    """Wczytuje listę użytkowników zapisanych na Airdrop z pliku."""
    try:
        with open("airdrop_list.txt", "r") as file:
            for line in file:
                airdrop_list.append(int(line.strip()))
    except FileNotFoundError:
        pass

# Funkcja startowa
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to FutureGreen Bot! 🌱\n"
        "Use /subscribe to receive updates about FGN, /menu to explore options, and /airdrop to join the Airdrop!"
    )

# Funkcja zapisu na Airdrop
async def airdrop_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in airdrop_list:
        airdrop_list.append(chat_id)
        await update.message.reply_text("🎉 You've been successfully registered for the FutureGreen Airdrop! 🚀")
        save_airdrop_list()
    else:
        await update.message.reply_text("You're already registered for the Airdrop! ✅")

# Funkcja statystyk Airdrop
async def airdrop_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_users = len(airdrop_list)
    await update.message.reply_text(f"📊 Total registered for the Airdrop: {total_users}")

# Funkcja menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Visit Website", url="https://futuregreen.fun")],
        [InlineKeyboardButton("Join Telegram", url="https://t.me/FutureGreenFGN")],
        [InlineKeyboardButton("Follow on X", url="https://x.com/FutureGreenFGN")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌿 Choose an option:", reply_markup=reply_markup)

# Główna funkcja
def main():
    # Wczytanie listy Airdrop przy starcie
    load_airdrop_list()

    # Tworzymy aplikację
    application = Application.builder().token(API_TOKEN).build()

    # Dodajemy obsługę komend
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("airdrop", airdrop_register))
    application.add_handler(CommandHandler("airdrop_stats", airdrop_stats))
    application.add_handler(CommandHandler("menu", menu))

    # Uruchamiamy bota
    application.run_polling()

if __name__ == '__main__':
    main()
