import os
import re
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from services.downloader import download_instagram_video
from services.messages import get_random_warning

router = Router()

# Regex to find instagram URLs
IG_LINK_PATTERN = r"(https?://(?:www\.)?instagram\.com/[^\s]+)"

@router.message(F.text.regexp(IG_LINK_PATTERN))
async def instagram_link_handler(message: Message):
    # Extract the first link found
    match = re.search(IG_LINK_PATTERN, message.text)
    if not match:
        return

    url = match.group(0)
    
    # Notify user we are processing
    status_msg = await message.reply("⏳ Video yuklanmoqda... Iltimos kuting.")
    
    try:
        # Download video
        video_path = download_instagram_video(url)
        
        if not video_path:
            await status_msg.edit_text("❌ Videoni yuklab bo'lmadi. Link yopiq profildan yoki noto'g'ri bo'lishi mumkin.")
            return

        # Prepare caption with warning
        caption = get_random_warning()
        
        # Send video
        video_input = FSInputFile(video_path)
        await message.reply_video(video=video_input, caption=caption, parse_mode="Markdown")
        
        # Delete the status message
        await status_msg.delete()
        
        # Optional: cleanup file immediately or rely on next run cleanup
        try:
            os.remove(video_path)
        except:
            pass
            
    except Exception as e:
        await status_msg.edit_text(f"❌ Xatolik yuz berdi: {str(e)}")
        # In production logging is better than sending raw error to user
