from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pandas as pd
import os

df = pd.read_excel("dorilar.xlsx")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Salom! Men dorilar haqida ma'lumot beruvchi botman. "
        "Dorani nomini yozing va men sizga mavjudligi, narxi va retsepli/retsepsiz ekanligini aytaman."
    )

def search_drug(update: Update, context: CallbackContext):
    user_input = update.message.text.lower()
    
    match = df[df['Nomi'].str.lower() == user_input]
    
    if match.empty:
        update.message.reply_text(f"Kechirasiz, {user_input} nomli dori topilmadi.")
    else:
        row = match.iloc[0]
        message = f"**{row['Nomi']}** dorisi mavjud!\n"
        message += f"Narxi: {row['Narxi']} so'm\n"
        message += f"Dona/Pachka: {row['Dona/Pachka']}\n"
        message += f"Retsepsiz/Retsepli: {row['Retsepsiz/Retsepli']}\n"
        message += "Filiallardagi narxlari:\n"
        for i in range(1, 7):
            message += f"Filial {i}: {row[f'Filial{i}']} so'm\n"
        
        update.message.reply_text(message)

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    updater = Updater(TOKEN, use_context=True)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_drug))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
