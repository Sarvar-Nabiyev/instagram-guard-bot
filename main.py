import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from handlers import commands, links

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token or token == "your_bot_token_here":
        logger.error("BOT_TOKEN is not set in .env file!")
        print("❌ Iltimos, .env fayliga BOT_TOKEN ni yozing!")
        return

    bot = Bot(token=token)
    dp = Dispatcher()

    # Register routers
    dp.include_router(commands.router)
    dp.include_router(links.router)

    # Start polling
    logger.info("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi")
