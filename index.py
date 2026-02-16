from telegram import Bot
import asyncio
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(TOKEN)

async def cleanup():
    # webhookni async tarzda o'chirish
    await bot.delete_webhook(drop_pending_updates=True)

asyncio.run(cleanup())
