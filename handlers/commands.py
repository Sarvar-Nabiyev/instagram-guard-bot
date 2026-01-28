import os
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.stats import get_stats, format_stats_message

router = Router()

# Admin user ID - faqat shu user /stats ko'ra oladi
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Assalomu alaykum! Men Instagram Guardian botman.\n\n"
        "Meni guruhlarga qo'shing. Men guruhdagi Instagram linklarini topib, "
        "videolarni yuklab beraman va Instagramning zararlari haqida eslatib turaman."
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Meni ishlashim uchun shunchaki guruhga qo'shing va admin huquqini bering "
        "(xabarlarni o'qish va yozish uchun).\n\n"
        "Men guruhga tashlangan har qanday `instagram.com` linkini avtomatik ushlayman."
    )

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Admin uchun statistika ko'rsatish"""
    user_id = message.from_user.id
    
    # Faqat admin ko'ra oladi
    if ADMIN_USER_ID and user_id != ADMIN_USER_ID:
        await message.answer("⛔ Bu buyruq faqat admin uchun.")
        return
    
    try:
        stats = get_stats()
        stats_message = format_stats_message(stats)
        await message.answer(stats_message, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Statistikani olishda xatolik: {str(e)}")
