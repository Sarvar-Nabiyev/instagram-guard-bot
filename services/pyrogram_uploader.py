"""
Pyrogram client for uploading large files (up to 2GB)
Uses MTProto protocol instead of Bot API
"""

import os
import asyncio
import logging
from pyrogram import Client
from pyrogram.errors import FloodWait

logger = logging.getLogger(__name__)

# Singleton client instance
_client: Client = None
_client_lock = asyncio.Lock()


async def get_pyrogram_client() -> Client:
    """Get or create Pyrogram client instance"""
    global _client
    
    async with _client_lock:
        if _client is None:
            api_id = os.getenv("API_ID")
            api_hash = os.getenv("API_HASH")
            bot_token = os.getenv("BOT_TOKEN")
            
            if not all([api_id, api_hash, bot_token]):
                logger.error("API_ID, API_HASH, or BOT_TOKEN not set for Pyrogram")
                return None
            
            # Create client with bot token
            _client = Client(
                name="instagram_guard_bot",
                api_id=int(api_id),
                api_hash=api_hash,
                bot_token=bot_token,
                workdir="data",  # Session file stored here
                no_updates=True  # We don't need updates, aiogram handles that
            )
            
            try:
                await _client.start()
                logger.info("Pyrogram client started successfully")
            except Exception as e:
                logger.error(f"Failed to start Pyrogram client: {e}")
                _client = None
                return None
        
        return _client


async def upload_large_video(chat_id: int, video_path: str, caption: str = None) -> bool:
    """
    Upload video using Pyrogram (supports up to 2GB)
    
    Args:
        chat_id: Telegram chat ID to send video to
        video_path: Path to the video file
        caption: Optional caption for the video
        
    Returns:
        True if successful, False otherwise
    """
    client = await get_pyrogram_client()
    
    if client is None:
        logger.error("Pyrogram client not available")
        return False
    
    try:
        # Get file size
        file_size = os.path.getsize(video_path)
        file_size_mb = file_size / (1024 * 1024)
        
        logger.info(f"Uploading {file_size_mb:.1f} MB video via Pyrogram")
        
        # Upload with progress
        await client.send_video(
            chat_id=chat_id,
            video=video_path,
            caption=caption,
            parse_mode="markdown",
            supports_streaming=True
        )
        
        logger.info(f"Successfully uploaded {file_size_mb:.1f} MB video")
        return True
        
    except FloodWait as e:
        logger.warning(f"FloodWait: sleeping for {e.value} seconds")
        await asyncio.sleep(e.value)
        # Retry once after flood wait
        try:
            await client.send_video(
                chat_id=chat_id,
                video=video_path,
                caption=caption,
                parse_mode="markdown",
                supports_streaming=True
            )
            return True
        except Exception as retry_error:
            logger.error(f"Retry failed: {retry_error}")
            return False
            
    except Exception as e:
        logger.error(f"Pyrogram upload failed: {e}")
        return False


async def stop_pyrogram_client():
    """Stop Pyrogram client gracefully"""
    global _client
    
    async with _client_lock:
        if _client is not None:
            try:
                await _client.stop()
                logger.info("Pyrogram client stopped")
            except Exception as e:
                logger.error(f"Error stopping Pyrogram client: {e}")
            finally:
                _client = None
