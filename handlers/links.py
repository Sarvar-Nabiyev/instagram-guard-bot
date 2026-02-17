import os
import re
import logging
import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from services.downloader import download_video, download_audio
from services.messages import get_random_warning
from services.stats import track_request
from services.pyrogram_uploader import upload_large_video, upload_large_audio, create_progress_bar

router = Router()
logger = logging.getLogger(__name__)

# Regex to find instagram URLs
LINK_PATTERN = r"(https?://(?:www\.)?(?:instagram\.com)/[^\s]+)"
# Regex to find YouTube URLs (handles m.youtube.com, etc)
# Limit concurrent processing to 2 to avoid IP bans and overload
_download_sem = asyncio.Semaphore(2)

# Report keyboard for error messages
REPORT_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✍️ Xatolikni xabar berish", callback_data="report_error")]
])


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
    # Block specific user
    if message.from_user.id == 7065956674:
        return

    # Send format selection buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📹 Video (480p)", callback_data="dl_video"),
            InlineKeyboardButton(text="🎵 Audio (MP3)", callback_data="dl_audio")
        ]
    ])
    
    await message.reply(
        "Formatni tanlang:",
        reply_markup=keyboard
    )


@router.callback_query(F.data.in_({"dl_video", "dl_audio"}))
async def callback_download(callback: CallbackQuery):
    # Verify original message exists
    if not callback.message.reply_to_message or not callback.message.reply_to_message.text:
        await callback.message.edit_text("❌ Original xabar o'chirilgan yoki topilmadi.", reply_markup=REPORT_KEYBOARD)
        return

    # Extract URL from original message
    match = re.search(LINK_PATTERN, callback.message.reply_to_message.text)
    if not match:
        await callback.message.edit_text("❌ Havola topilmadi.", reply_markup=REPORT_KEYBOARD)
        return
        
    url = match.group(0)
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    
    await callback.message.edit_text("⏳ Yuklanmoqda...")
    
    if callback.data == "dl_video":
        await process_video(callback.message, url, user_id, chat_id)
    else:
        await process_audio(callback.message, url, user_id, chat_id)


async def process_video(status_msg: Message, url: str, user_id: int, chat_id: int):
    try:
        video_path = None
        video_caption = None
        
        async with _download_sem:
            max_retries = 5
            backoff = 5
            
            for attempt in range(max_retries):
                result = download_video(url)
                
                if result:
                    video_path = result['path']
                    video_caption = result['caption']
                    break
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff)
                    backoff *= 2
        
        # Custom Caption Logic
        footer = "\n<a href='https://t.me/vid_instagrambot'>@vid_instagrambot</a>"
        if video_caption:
            # Escape and wrap in expandable blockquote (full text)
            import html
            safe_caption = html.escape(video_caption)
            video_caption = f"<blockquote expandable>{safe_caption}</blockquote>{footer}"
        else:
            video_caption = footer
        
        if not video_path:
            track_request(user_id, success=False, request_type='video_download')
            await status_msg.edit_text("❌ Videoni yuklab bo'lmadi.", reply_markup=REPORT_KEYBOARD)
            return

        file_size_mb = get_file_size_mb(video_path)
        logger.info(f"Uploading {file_size_mb:.1f} MB video")
        
        async def update_progress(current, total, percent, speed, eta):
            try:
                current_mb = current / (1024 * 1024)
                total_mb = total / (1024 * 1024)
                progress_bar = create_progress_bar(percent)
                eta_str = format_time(eta) if eta > 0 else "hisoblanmoqda..."
                
                text = (
                    f"📹 <b>Video yuklanmoqda...</b>\n\n"
                    f"{progress_bar} <b>{percent:.0f}%</b>\n\n"
                    f"📊 {current_mb:.1f} / {total_mb:.1f} MB\n"
                    f"⚡ {speed:.1f} MB/s\n"
                    f"⏱ ~{eta_str}"
                )
                await status_msg.edit_text(text, parse_mode="HTML")
            except:
                pass
        
        success = await upload_large_video(chat_id, video_path, video_caption, update_progress)
        
        if success:
            track_request(user_id, success=True, request_type='video_download')
            await status_msg.delete()
            
            try:
                warning = get_random_warning()
                await status_msg.bot.send_message(chat_id, warning, parse_mode="HTML")
            except:
                pass
        else:
            track_request(user_id, success=False, request_type='video_download')
            await status_msg.edit_text("❌ Video yuklashda xatolik yuz berdi.", reply_markup=REPORT_KEYBOARD)
        
        try:
            os.remove(video_path)
        except:
            pass
            
    except Exception as e:
        logger.error(f"Error in process_video: {e}")
        track_request(user_id, success=False, request_type='video_download')
        await status_msg.edit_text("❌ Xatolik yuz berdi.", reply_markup=REPORT_KEYBOARD)


async def process_audio(status_msg: Message, url: str, user_id: int, chat_id: int):
    try:
        audio_path = None
        caption = None
        performer = None
        title = None
        
        async with _download_sem:
            max_retries = 5
            backoff = 5
            
            for attempt in range(max_retries):
                result = download_audio(url)
                
                if result:
                    audio_path = result['path']
                    caption = result['caption']
                    performer = result['performer']
                    title = result['title']
                    break
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff)
                    backoff *= 2
        
        if not audio_path:
            track_request(user_id, success=False, request_type='audio_download')
            await status_msg.edit_text("❌ Audioni yuklab bo'lmadi.", reply_markup=REPORT_KEYBOARD)
            return

        file_size_mb = get_file_size_mb(audio_path)
        logger.info(f"Uploading {file_size_mb:.1f} MB audio")
        
        # Custom Caption Logic for Audio (same as Video)
        footer = "\n<a href='https://t.me/vid_instagrambot'>@vid_instagrambot</a>"
        if caption:
            import html
            safe_caption = html.escape(caption)
            caption = f"<blockquote expandable>{safe_caption}</blockquote>{footer}"
        else:
            caption = footer
        
        async def update_progress(current, total, percent, speed, eta):
            try:
                progress_bar = create_progress_bar(percent)
                text = (
                    f"🎵 <b>Audio yuklanmoqda...</b>\n\n"
                    f"{progress_bar} <b>{percent:.0f}%</b>"
                )
                await status_msg.edit_text(text, parse_mode="HTML")
            except:
                pass
        
        success = await upload_large_audio(
            chat_id, audio_path, caption, performer, title, update_progress
        )
        
        if success:
            track_request(user_id, success=True, request_type='audio_download')
            await status_msg.delete()
            
            # Send warning for audio too? Logic says yes because using social media.
            # But maybe less intrusive. Let's send it.
            try:
                warning = get_random_warning()
                await status_msg.bot.send_message(chat_id, warning, parse_mode="HTML")
            except:
                pass
        else:
            track_request(user_id, success=False, request_type='audio_download')
            await status_msg.edit_text("❌ Audio yuklashda xatolik yuz berdi.", reply_markup=REPORT_KEYBOARD)
        
        try:
            os.remove(audio_path)
        except:
            pass
            
    except Exception as e:
        logger.error(f"Error in process_audio: {e}")
        track_request(user_id, success=False, request_type='audio_download')
        await status_msg.edit_text("❌ Xatolik yuz berdi.", reply_markup=REPORT_KEYBOARD)
