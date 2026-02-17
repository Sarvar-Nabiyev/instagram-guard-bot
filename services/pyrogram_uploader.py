"""
Pyrogram client for uploading large files (up to 2GB)
Uses MTProto protocol instead of Bot API
"""

import os
import asyncio
import logging
import time
from typing import Callable, Optional
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait

logger = logging.getLogger(__name__)

# Singleton client instance
_client: Client = None
_client_lock = asyncio.Lock()
# Lock to ensure sequential uploads (Pyrogram client limitation workaround)
_upload_lock = asyncio.Lock()


def create_progress_bar(percent: float, length: int = 10) -> str:
    """Create a visual progress bar"""
    filled = int(length * percent / 100)
    empty = length - filled
    bar = "█" * filled + "░" * empty
    return bar


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


async def upload_large_video(
    chat_id: int, 
    video_path: str, 
    caption: str = None,
    progress_callback: Optional[Callable] = None
) -> bool:
    """
    Upload video using Pyrogram (supports up to 2GB)
    
    Args:
        chat_id: Telegram chat ID to send video to
        video_path: Path to the video file
        caption: Optional caption for the video
        progress_callback: Optional async callback for progress updates
            Will be called with (current_bytes, total_bytes, percent, speed_mbps)
        
    Returns:
        True if successful, False otherwise
    """
    client = await get_pyrogram_client()
    
    if client is None:
        logger.error("Pyrogram client not available")
        return False

    # Track progress state
    progress_state = {
        'last_update': 0,
        'start_time': time.time(),
        'last_bytes': 0
    }
    
    async def progress_handler(current: int, total: int):
        """Internal progress handler"""
        now = time.time()
        
        # Update every 2 seconds to avoid rate limits
        if now - progress_state['last_update'] < 2:
            return
        
        progress_state['last_update'] = now
        
        # Calculate progress
        percent = (current / total) * 100 if total > 0 else 0
        
        # Calculate speed
        elapsed = now - progress_state['start_time']
        speed_mbps = (current / (1024 * 1024)) / elapsed if elapsed > 0 else 0
        
        # Estimate remaining time
        if speed_mbps > 0:
            remaining_mb = (total - current) / (1024 * 1024)
            eta_seconds = remaining_mb / speed_mbps
        else:
            eta_seconds = 0
        
        # Call callback if provided
        if progress_callback:
            try:
                await progress_callback(current, total, percent, speed_mbps, eta_seconds)
            except Exception as e:
                logger.warning(f"Progress callback error: {e}")

    # Use lock to process one upload at a time
    async with _upload_lock:
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Get file size
                file_size = os.path.getsize(video_path)
                file_size_mb = file_size / (1024 * 1024)
                
                logger.info(f"Uploading {file_size_mb:.1f} MB video via Pyrogram (Attempt {attempt+1}/{max_retries})")
                
                # Reset progress state for retry
                progress_state['start_time'] = time.time()
                progress_state['last_update'] = 0
                
                # Upload with progress
                await client.send_video(
                    chat_id=chat_id,
                    video=video_path,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    supports_streaming=True,
                    progress=progress_handler
                )
                
                logger.info(f"Successfully uploaded {file_size_mb:.1f} MB video")
                return True
                
            except FloodWait as e:
                wait_time = e.value + 2
                logger.warning(f"FloodWait: sleeping for {wait_time} seconds before retry")
                await asyncio.sleep(wait_time)
                # Continue to next attempt
                
            except Exception as e:
                logger.error(f"Pyrogram upload failed (Attempt {attempt+1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)  # Wait briefly before retry
                else:
                    return False
        
                return False
        
        return False


async def upload_large_audio(
    chat_id: int, 
    audio_path: str,
    caption: str = None,
    performer: str = None,
    title: str = None,
    progress_callback: Optional[Callable] = None
) -> bool:
    """
    Upload audio using Pyrogram
    """
    client = await get_pyrogram_client()
    
    if client is None:
        logger.error("Pyrogram client not available")
        return False

    # Track progress state
    progress_state = {
        'last_update': 0,
        'start_time': time.time(),
        'last_bytes': 0
    }
    
    async def progress_handler(current: int, total: int):
        """Internal progress handler"""
        now = time.time()
        
        # Update every 2 seconds to avoid rate limits
        if now - progress_state['last_update'] < 2:
            return
        
        progress_state['last_update'] = now
        
        # Calculate progress
        percent = (current / total) * 100 if total > 0 else 0
        
        # Calculate speed
        elapsed = now - progress_state['start_time']
        speed_mbps = (current / (1024 * 1024)) / elapsed if elapsed > 0 else 0
        
        # Estimate remaining time
        if speed_mbps > 0:
            remaining_mb = (total - current) / (1024 * 1024)
            eta_seconds = remaining_mb / speed_mbps
        else:
            eta_seconds = 0
        
        # Call callback if provided
        if progress_callback:
            try:
                await progress_callback(current, total, percent, speed_mbps, eta_seconds)
            except Exception as e:
                logger.warning(f"Progress callback error: {e}")

    # Use lock to process one upload at a time
    async with _upload_lock:
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Uploading audio via Pyrogram (Attempt {attempt+1}/{max_retries})")
                
                # Reset progress state
                progress_state['start_time'] = time.time()
                progress_state['last_update'] = 0
                
                await client.send_audio(
                    chat_id=chat_id,
                    audio=audio_path,
                    caption=caption,
                    title=title,
                    performer=performer,
                    parse_mode=ParseMode.HTML,
                    progress=progress_handler
                )
                
                logger.info(f"Successfully uploaded audio")
                return True
                
            except FloodWait as e:
                wait_time = e.value + 2
                logger.warning(f"FloodWait: sleeping for {wait_time} seconds before retry")
                await asyncio.sleep(wait_time)
                
            except Exception as e:
                logger.error(f"Pyrogram audio upload failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                else:
                    return False
        
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
