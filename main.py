import asyncio
import logging
import os
from dotenv import load_dotenv
from aiohttp import web
from aiogram import Bot, Dispatcher
from handlers import commands, links, groups
from services.stats import init_db
from services.pyrogram_uploader import get_pyrogram_client, stop_pyrogram_client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize statistics database
init_db()
logger.info("Statistics database initialized")

async def start_webhook():
    """
    Simple dummy web server to satisfy cloud providers (Render/Railway)
    that require binding to a specific port.
    """
    app = web.Application()
    async def handle_health(request):
        return web.Response(text="Bot is running OK")
    
    app.router.add_get('/', handle_health)
    app.router.add_get('/health', handle_health)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Web server running on port {port}")

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        logger.error("BOT_TOKEN environment variable not set.")
        return

    bot = Bot(token=token)
    dp = Dispatcher()

    # Register routers
    dp.include_router(commands.router)
    dp.include_router(links.router)
    dp.include_router(groups.router)

    # Start web server for cloud port binding
    await start_webhook()
    
    # Initialize Pyrogram client for large file uploads
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    if api_id and api_hash:
        pyrogram_client = await get_pyrogram_client()
        if pyrogram_client:
            logger.info("Pyrogram client ready for large file uploads (up to 2GB)")
        else:
            logger.warning("Pyrogram client failed to start, large files won't work")
    else:
        logger.warning("API_ID/API_HASH not set, large file upload disabled")

    # Start polling
    logger.info("Bot ishga tushdi...")
    try:
        await dp.start_polling(bot)
    finally:
        # Graceful shutdown
        await stop_pyrogram_client()
        logger.info("Cleanup completed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi")

