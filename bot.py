from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import pandas as pd
import os

# Excel faylini o'qish
df = pd.read_excel("dorilar.xlsx")

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men dorilar haqida ma'lumot beruvchi botman.\n"
        "Dorani nomini yozing va men sizga mavjudligi, narxi va ishlab chiqaruvchisi va boshqa ma'lumotlarni aytaman."
    )

# Dorani qidirish
async def search_drug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().lower()

    df['Наименование'] = df['Наименование'].fillna("").astype(str)

    match = df[df['Наименование'].str.lower().str.contains(user_input, na=False)]

    if match.empty:
        await update.message.reply_text(f"Kechirasiz, '{user_input}' nomli dori topilmadi.")
    else:
        message = ""
        for idx, row in match.iterrows():
            message += f"{row['Наименование']} dorisi mavjud!\n"
            message += f"Narxi: {row['Цена']} so'm\n"
            message += f"Amal qilish muddati: {row['Срок годности']}\n"
            message += f"Ishlab chiqaruvchi: {row['Производитель']}\n"
            message += f"Yetkazib berish sanasi: {row['Дата поставки']}\n\n"

        await update.message.reply_text(message)

# Bot ishga tushishi
def main():
    # Tokenni to'g'ridan-to'g'ri qo'ying yoki atrof-muhitdan oling
    TOKEN = os.environ.get("BOT_TOKEN") or "SIZNING_TOKENINGIZ_SHU YERGA"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_drug))
    
    # Polling boshlanadi
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
