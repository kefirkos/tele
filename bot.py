import os
import http.server
import socketserver
import threading
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Token API
API_TOKEN = '7697064545:AAHWQCDqr5BYYqqmvU_Kc-Oah9aWb40k5rU'

# Listy subskrybentów i zapisanych na Airdrop (z adresami Solana)
SUBSCRIBERS = []
airdrop_list = {}  # Słownik: {chat_id: address}

# Funkcje zapisu/odczytu Airdrop
def save_airdrop_list():
    """Zapisuje listę użytkowników zapisanych na Airdrop (chat_id i adresy Solana) do pliku."""
    with open("airdrop_list.txt", "w") as file:
        for chat_id, address in airdrop_list.items():
            file.write(f"{chat_id}:{address}\n")

def load_airdrop_list():
    """Wczytuje listę użytkowników zapisanych na Airdrop z pliku."""
    try:
        with open("airdrop_list.txt", "r") as file:
            for line in file:
                chat_id, address = line.strip().split(":")
                airdrop_list[int(chat_id)] = address
    except FileNotFoundError:
        pass

# Funkcja startowa
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to FutureGreen Bot! 🌱\n"
        "Use /subscribe to receive updates about FGN, /menu to explore options, and /airdrop to join the Airdrop!"
    )

# Funkcja zapisu na Airdrop (rozpoczęcie procesu)
async def airdrop_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in airdrop_list:
        await update.message.reply_text("You're already registered for the Airdrop! ✅")
    else:
        await update.message.reply_text(
            "Please enter your Solana wallet address to register for the FutureGreen Airdrop: 🚀"
        )
        # Przechodzimy w stan oczekiwania na wiadomość od użytkownika
        return

# Funkcja do obsługi wpisywania adresu Solana
async def handle_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    address = update.message.text

    # Prosta walidacja adresu (Solana adresy mają zwykle 43-44 znaki i są alfanumeryczne)
    if len(address) >= 43 and len(address) <= 44 and address.isalnum():
        airdrop_list[chat_id] = address
        save_airdrop_list()
        await update.message.reply_text("🎉 You've been successfully registered for the FutureGreen Airdrop! 🚀")
    else:
        await update.message.reply_text("❌ Invalid wallet address. Please try again.")

# Funkcja statystyk Airdrop
async def airdrop_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_users = len(airdrop_list)
    await update.message.reply_text(f"📊 Total registered for the Airdrop: {total_users}")

# Funkcja menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Visit Website", url="https://futuregreen.fun")],
        [InlineKeyboardButton("Join Telegram", url="https://t.me/FutureGreenFGN")],
        [InlineKeyboardButton("Follow on X", url="https://x.com/FutureGreenFGN")],
        [InlineKeyboardButton("Join Airdrop", callback_data="join_airdrop")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌿 Choose an option:", reply_markup=reply_markup)

# Obsługa przycisku "Join Airdrop"
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "join_airdrop":
        await query.message.reply_text(
            "To join the Airdrop, please enter your Solana wallet address:"
        )

# Prosty serwer HTTP działający w tle
def run_http_server():
    PORT = 8000  # Domyślny port HTTP
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving HTTP on port {PORT}")
        httpd.serve_forever()

# Główna funkcja
def main():
    # Wczytanie listy Airdrop przy starcie
    load_airdrop_list()

    # Uruchom serwer HTTP w tle
    threading.Thread(target=run_http_server, daemon=True).start()

    while True:  # Pętla ponawiająca połączenie
        try:
            # Tworzymy aplikację
            application = Application.builder().token(API_TOKEN).build()

            # Dodajemy obsługę komend
            application.add_handler(CommandHandler("start", start))
            application.add_handler(CommandHandler("airdrop", airdrop_register))
            application.add_handler(CommandHandler("airdrop_stats", airdrop_stats))
            application.add_handler(CommandHandler("menu", menu))

            # Dodajemy obsługę wiadomości użytkownika (adresy Solana)
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet_address))

            # Obsługa przycisków
            application.add_handler(CommandHandler("button", handle_button))

            # Uruchamiamy bota
            application.run_polling()
        except Exception as e:
            print(f"Bot disconnected due to error: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == '__main__':
    main()
