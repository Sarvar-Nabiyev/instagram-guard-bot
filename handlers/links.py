import os
import re
import logging
from aiogram import Router, F
from aiogram.types import Message
from services.downloader import download_video
from services.messages import get_random_warning
from services.stats import track_request
from services.pyrogram_uploader import upload_large_video, create_progress_bar

router = Router()
logger = logging.getLogger(__name__)

# Regex to find instagram URLs
LINK_PATTERN = r"(https?://(?:www\.)?(?:instagram\.com)/[^\s]+)"


def get_file_size_mb(path: str) -> float:
    """Get file size in MB"""
    return os.path.getsize(path) / (1024 * 1024)


def format_time(seconds: float) -> str:
    """Format seconds to human readable time"""
    if seconds < 60:
        return f"{int(seconds)} soniya"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes} daqiqa {secs} soniya"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours} soat {minutes} daqiqa"


@router.message(F.text.regexp(LINK_PATTERN))
async def link_handler(message: Message):
    # Extract the first link found
    match = re.search(LINK_PATTERN, message.text)
    if not match:
        return

    url = match.group(0)
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # Notify user we are processing
    status_msg = await message.reply("⏳ Instagram'dan video yuklanmoqda...")
    
    try:
        # Download video from Instagram
        video_path = download_video(url)
        
        if not video_path:
            # Track failed request
            track_request(user_id, success=False, request_type='video_download')
            await status_msg.edit_text("❌ Videoni yuklab bo'lmadi. Link yopiq profildan yoki noto'g'ri bo'lishi mumkin.")
            return

        # Get file size
        file_size_mb = get_file_size_mb(video_path)
        
        # Prepare caption with warning
        caption = get_random_warning()
        
        # Log upload start
        logger.info(f"Uploading {file_size_mb:.1f} MB video via Pyrogram")
        
        # Create progress callback for ALL videos
        async def update_progress(current: int, total: int, percent: float, speed: float, eta: float):
            """Update status message with progress"""
            try:
                current_mb = current / (1024 * 1024)
                total_mb = total / (1024 * 1024)
                progress_bar = create_progress_bar(percent)
                eta_str = format_time(eta) if eta > 0 else "hisoblanmoqda..."
                
                progress_text = (
                    f"📤 **Telegram'ga yuklanmoqda...**\n\n"
                    f"{progress_bar} **{percent:.0f}%**\n\n"
                    f"📊 {current_mb:.1f} / {total_mb:.1f} MB\n"
                    f"⚡ Tezlik: {speed:.1f} MB/s\n"
                    f"⏱ Qoldi: ~{eta_str}"
                )
                
                await status_msg.edit_text(progress_text, parse_mode="Markdown")
            except Exception as e:
                # Ignore edit errors (too frequent, message not modified, etc.)
                pass
        
        # Initial upload message
        await status_msg.edit_text(
            f"📤 **Telegram'ga yuklanmoqda...**\n\n"
            f"░░░░░░░░░░ **0%**\n\n"
            f"📊 0 / {file_size_mb:.1f} MB\n"
            f"⚡ Tezlik: hisoblanmoqda...\n"
            f"⏱ Qoldi: hisoblanmoqda...",
            parse_mode="Markdown"
        )
        
        # Use Pyrogram for ALL videos to show progress
        success = await upload_large_video(chat_id, video_path, caption, update_progress)
        
        if success:
            # Track successful request
            track_request(user_id, success=True, request_type='video_download')
            await status_msg.delete()
        else:
            # Pyrogram failed, track as failed
            track_request(user_id, success=False, request_type='video_download')
            await status_msg.edit_text(
                "❌ Video yuklashda xatolik yuz berdi. Keyinroq qayta urinib ko'ring."
            )
        
        # Cleanup file
        try:
            os.remove(video_path)
        except:
            pass
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in link_handler: {error_msg}")
        
        # Track failed request
        track_request(user_id, success=False, request_type='video_download')
        
        # Check for file size limit error
        if "Request Entity Too Large" in error_msg or "too large" in error_msg.lower():
            await status_msg.edit_text(
                "⚠️ **Video hajmi juda katta!**\n\n"
                "2 GB dan katta videolarni yuklab bo'lmaydi.\n\n"
                "💡 **Yechim:** Qisqaroq video tanlang.",
                parse_mode="Markdown"
            )
        else:
            await status_msg.edit_text(f"❌ Xatolik yuz berdi: {error_msg}")
