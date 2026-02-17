import os
import logging
from aiogram import Router, F, Bot
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()
logger = logging.getLogger(__name__)

ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))

class ReportStates(StatesGroup):
    waiting_for_report = State()
    admin_replying = State()

@router.message(Command("report"))
async def cmd_report(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_USER_ID:
        await message.answer("🛠️ Siz adminsiz, report yuborib nima qilasiz? :)")
        return
        
    await message.answer(
        "📝 <b>Xatolik haqida xabar berish</b>\n\n"
        "Iltimos, muammoni batafsil tushuntirib yozing (yoki rasm yuboring).\n"
        "Sizning xabaringiz to'g'ridan-to'g'ri adminga yetkaziladi.\n\n"
        "Bekor qilish uchun /cancel deb yozing.",
        parse_mode="HTML"
    )
    await state.set_state(ReportStates.waiting_for_report)

@router.message(Command("cancel"), ReportStates.waiting_for_report)
async def cancel_report(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Bekor qilindi.")

@router.callback_query(F.data == "report_error")
async def callback_report_error(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        "📝 <b>Xatolik haqida xabar berish</b>\n\n"
        "Iltimos, muammoni batafsil tushuntirib yozing (yoki rasm yuboring).\n"
        "Sizning xabaringiz to'g'ridan-to'g'ri adminga yetkaziladi.\n\n"
        "Bekor qilish uchun /cancel deb yozing.",
        parse_mode="HTML"
    )
    await state.set_state(ReportStates.waiting_for_report)

@router.message(ReportStates.waiting_for_report)
async def process_report(message: Message, state: FSMContext, bot: Bot):
    if not ADMIN_USER_ID:
        await message.answer("⚠️ Admin ID sozlanmagan, report yuborib bo'lmaydi.")
        await state.clear()
        return

    # User info
    user = message.from_user
    username = f"@{user.username}" if user.username else "Username yo'q"
    user_info = f"👤 <b>Yangi Report!</b>\n\n<b>Kimdan:</b> {user.full_name} ({username})\n<b>ID:</b> <code>{user.id}</code>\n\n"

    reply_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Javob berish", callback_data=f"reply_to:{user.id}")]
    ])

    try:
        # Send info header with reply button
        await bot.send_message(ADMIN_USER_ID, user_info, parse_mode="HTML", reply_markup=reply_button)
        
        # Forward the actual message
        await bot.copy_message(
            chat_id=ADMIN_USER_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        
        await message.answer("✅ <b>Xabaringiz adminga yuborildi.</b>\nTez orada ko'rib chiqamiz. Rahmat!", parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error forwarding report: {e}")
        await message.answer("❌ Xabarni yuborishda xatolik yuz berdi. Keyinroq qayta urinib ko'ring.")
    
    await state.clear()


@router.callback_query(F.data.startswith("reply_to:"))
async def callback_reply_to_user(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_USER_ID:
        await callback.answer("⛔ Faqat admin javob berishi mumkin.", show_alert=True)
        return
    
    target_user_id = int(callback.data.split(":")[1])
    await state.update_data(reply_target=target_user_id)
    await state.set_state(ReportStates.admin_replying)
    
    await callback.answer()
    await callback.message.answer(
        f"✏️ Foydalanuvchiga (<code>{target_user_id}</code>) javob yozing.\n"
        "Bekor qilish uchun /cancel deb yozing.",
        parse_mode="HTML"
    )


@router.message(Command("cancel"), ReportStates.admin_replying)
async def cancel_admin_reply(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Javob bekor qilindi.")


@router.message(ReportStates.admin_replying)
async def process_admin_reply(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    target_user_id = data.get("reply_target")
    
    if not target_user_id:
        await state.clear()
        return
    
    try:
        await bot.send_message(
            target_user_id,
            f"💬 <b>Admin javobi:</b>\n\n{message.text}",
            parse_mode="HTML"
        )
        await message.answer(f"✅ Javob yuborildi (user: <code>{target_user_id}</code>).", parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error replying to user {target_user_id}: {e}")
        await message.answer("❌ Javobni yuborishda xatolik. User botni block qilgan bo'lishi mumkin.")
    
    await state.clear()
