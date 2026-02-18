from telegram import Bot
import asyncio
import os

TOKEN = os.environ.get("8394683131:AAEcjffaHaqHiLvIP7JrTzql0OQTTzx7Euo")
bot = Bot(TOKEN)

async def cleanup():
    # webhookni async tarzda o'chirish
    await bot.delete_webhook(drop_pending_updates=True)

asyncio.run(cleanup())
