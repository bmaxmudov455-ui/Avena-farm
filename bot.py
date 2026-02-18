import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8394683131:AAEcjffaHaqHiLvIP7JrTzql0OQTTzx7Euo"

# Filiallar bazasi (namuna)
branches = {
    "bam bozorchasi ": {
        "address": "KIMYOGARLAR 44-A",
        "phone": "+998 662250261",
        "medicines": {
            "sitramon": "15 000 so'm",
            "traumel": "85 000 so'm"
        }
    },
    "SOGDIANA": {
        "address": "SOGDIANA ESKI BOVLING",
        "phone": "+998 90 1003654",
        "medicines": {
            "sitramon": "14 500 so'm",
            "traumel": "84 000 so'm"
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💊 Assalomu alaykum!\n"
        "Avena Farm botiga xush kelibsiz.\n\n"
        "Kerakli dorini nomini yozing."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    response = ""

    for BAM in BOZORCHASI, branch_info in branches.items():
        if user_text in branch_info["medicines"]:
            price = branch_info["medicines"][user_text]
            response += (
                f"🏥 Filial: {branch_name}\n"
                f"💰 Narxi: {price}\n"
                f"📍 Manzil: {branch_info['address']}\n"
                f"📞 Tel: {branch_info['phone']}\n\n"
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

if name == "main":
    main()