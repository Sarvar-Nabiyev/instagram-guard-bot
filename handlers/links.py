import os
import re
import logging
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from services.downloader import download_video
from services.messages import get_random_warning
from services.stats import track_request
from services.pyrogram_uploader import upload_large_video

router = Router()
logger = logging.getLogger(__name__)

# Regex to find instagram URLs
LINK_PATTERN = r"(https?://(?:www\.)?(?:instagram\.com)/[^\s]+)"

# File size threshold for using Pyrogram (45 MB to be safe)
LARGE_FILE_THRESHOLD = 45 * 1024 * 1024  # 45 MB in bytes


def get_file_size_mb(path: str) -> float:
    """Get file size in MB"""
    return os.path.getsize(path) / (1024 * 1024)


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
    status_msg = await message.reply("⏳ Video yuklanmoqda... Iltimos kuting.")
    
    try:
        # Download video
        video_path = download_video(url)
        
        if not video_path:
            # Track failed request
            track_request(user_id, success=False, request_type='video_download')
            await status_msg.edit_text("❌ Videoni yuklab bo'lmadi. Link yopiq profildan yoki noto'g'ri bo'lishi mumkin.")
            return

        # Get file size
        file_size = os.path.getsize(video_path)
        file_size_mb = get_file_size_mb(video_path)
        
        # Prepare caption with warning
        caption = get_random_warning()
        
        # Check if file is too large for Bot API
        if file_size > LARGE_FILE_THRESHOLD:
            # Use Pyrogram for large files
            logger.info(f"Large file detected ({file_size_mb:.1f} MB), using Pyrogram")
            await status_msg.edit_text(f"📤 Katta video yuklanmoqda ({file_size_mb:.1f} MB)... Biroz kuting.")
            
            success = await upload_large_video(chat_id, video_path, caption)
            
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
        else:
            # Use regular Bot API for small files (faster)
            track_request(user_id, success=True, request_type='video_download')
            
            video_input = FSInputFile(video_path)
            await message.reply_video(video=video_input, caption=caption, parse_mode="Markdown")
            await status_msg.delete()
        
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
        
        # Check for file size limit error (fallback if Pyrogram wasn't used)
        if "Request Entity Too Large" in error_msg or "too large" in error_msg.lower():
            await status_msg.edit_text(
                "⚠️ **Video hajmi juda katta!**\n\n"
                "Videoni qayta yuklashda xatolik yuz berdi.\n\n"
                "💡 **Yechim:** Keyinroq qayta urinib ko'ring.",
                parse_mode="Markdown"
            )
        else:
            await status_msg.edit_text(f"❌ Xatolik yuz berdi: {error_msg}")
