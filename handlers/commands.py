from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

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
