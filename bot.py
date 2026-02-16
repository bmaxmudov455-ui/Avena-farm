import os
import pandas as pd
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Excel faylini o'qish
df = pd.read_excel("dorilar.xlsx")

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men dorilar haqida ma'lumot beruvchi botman. "
        "Dorani nomini yozing va men sizga mavjudligi, narxi va retsepli/retsepsiz ekanligini aytaman."
    )

# Dorani qidirish
async def search_drug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    match = df[df['Nomi'].str.lower() == user_input]

    if match.empty:
        await update.message.reply_text(f"Kechirasiz, {user_input} nomli dori topilmadi.")
    else:
        row = match.iloc[0]
        message = f"**{row['Nomi']}** dorisi mavjud!\n"
        message += f"Narxi: {row['Narxi']} so'm\n"
        message += f"Dona/Pachka: {row['Dona/Pachka']}\n"
        message += f"Retsepsiz/Retsepli: {row['Retsepsiz/Retsepli']}\n"
        message += "Filiallardagi narxlari:\n"
        for i in range(1, 7):
            message += f"Filial {i}: {row[f'Filial{i}']} so'm\n"
        await update.message.reply_text(message)

# Main
def main():
    TOKEN = os.environ.get("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_drug))

    # Start polling (sync)
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
