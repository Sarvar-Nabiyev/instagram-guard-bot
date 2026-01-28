import os
import re
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from services.downloader import download_video
from services.messages import get_random_warning
from services.stats import track_request

router = Router()

# Regex to find instagram URLs
LINK_PATTERN = r"(https?://(?:www\.)?(?:instagram\.com)/[^\s]+)"

@router.message(F.text.regexp(LINK_PATTERN))
async def link_handler(message: Message):
    # Extract the first link found
    match = re.search(LINK_PATTERN, message.text)
    if not match:
        return

    url = match.group(0)
    user_id = message.from_user.id
    
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

        # Track successful request
        track_request(user_id, success=True, request_type='video_download')
        
        # Prepare caption with warning
        caption = get_random_warning()
        
        # Send video
        video_input = FSInputFile(video_path)
        await message.reply_video(video=video_input, caption=caption, parse_mode="Markdown")
        
        # Delete the status message
        await status_msg.delete()
        
        # Cleanup file
        try:
            os.remove(video_path)
        except:
            pass
            
    except Exception as e:
        error_msg = str(e)
        # Track failed request
        track_request(user_id, success=False, request_type='video_download')
        
        # Check for file size limit error
        if "Request Entity Too Large" in error_msg or "too large" in error_msg.lower():
            await status_msg.edit_text(
                "⚠️ **Video hajmi juda katta!**\n\n"
                "Telegram 50 MB dan katta videolarni yuborishni qo'llab-quvvatlamaydi.\n\n"
                "💡 **Yechim:** Videoni Instagram'dan o'zingiz yuklab oling yoki qisqaroq video tanlang.",
                parse_mode="Markdown"
            )
        else:
            await status_msg.edit_text(f"❌ Xatolik yuz berdi: {error_msg}")
