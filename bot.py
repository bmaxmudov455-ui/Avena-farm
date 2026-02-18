import logging
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8394683131:AAEcjffaHaqHiLvIP7JrTzql0OQTTzx7Euo"

# Excel faylini o'qish
df = pd.read_excel("dorilar.xlsx")

# Foydalanuvchi yozgan matnni qidirib, kerakli ustunlar bilan ishlash
columns_to_use = ["№", "Nomi", "summa", "muddati", "davlati", "kelgan sanasi"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💊 Assalomu alaykum!\n"
        "Avena Farm botiga xush kelibsiz.\n\n"
        "Kerakli dorining nomini yozing (masalan: shprist)."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower().strip()
    response = ""

    for index, row in df.iterrows():
        if pd.notna(row["Nomi"]) and user_text in str(row["Nomi"]).lower():
            # Faqat kerakli ustunlarni chiqarish
            response += (
                f"📌 №: {row['№']}\n"
                f"💊 Nomi: {row['Nomi']}\n"
                f"💰 Summa: {row['summa']}\n"
                f"🗓 Muddati: {row['muddati']}\n"
                f"🌍 Davlati: {row['davlati']}\n"
                f"📅 Kelgan sanasi: {row['kelgan sanasi']}\n\n"
            )

    if response == "":
        response = "❌ Bu dori hozircha mavjud emas.\nIltimos, boshqa nom bilan tekshirib ko‘ring."

    await update.message.reply_text(response)

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
