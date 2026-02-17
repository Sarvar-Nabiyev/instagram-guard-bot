import os
import asyncio
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError

from services.stats import get_stats, format_stats_message, get_all_users, get_all_groups

router = Router()
logger = logging.getLogger(__name__)

ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))

class AdminStates(StatesGroup):
    waiting_for_ad_content = State()
    confirm_ad = State()
    waiting_for_link = State()

def get_admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📢 Reklama yuborish")],
            [KeyboardButton(text="🔗 Link yuborish")]
        ],
        resize_keyboard=True
    )

@router.message(F.text == "📊 Statistika", F.from_user.id == ADMIN_USER_ID)
async def msg_stats(message: Message):
    try:
        stats = get_stats()
        text = format_stats_message(stats)
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")

@router.message(F.text == "🔗 Link yuborish", F.from_user.id == ADMIN_USER_ID)
async def msg_link_prompt(message: Message):
    await message.answer("🔗 <b>Instagram linkini yuboring:</b>\n\nMen uni yuklab beraman.", parse_mode="HTML")

# --- Broadcasting Flow ---

@router.message(F.text == "📢 Reklama yuborish", F.from_user.id == ADMIN_USER_ID)
async def msg_broadcast(message: Message, state: FSMContext):
    await message.answer(
        "📢 <b>Reklama yuborish</b>\n\n"
        "Reklama postini yuboring (matn, rasm, video).\n"
        "Bekor qilish uchun /cancel ni bosing.",
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_ad_content)

@router.message(Command("cancel"), AdminStates.waiting_for_ad_content)
@router.message(Command("cancel"), AdminStates.confirm_ad)
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Bekor qilindi.", reply_markup=get_admin_keyboard())

@router.message(AdminStates.waiting_for_ad_content)
async def receive_ad_content(message: Message, state: FSMContext):
    # Store message ID and chat ID to copy later
    await state.update_data(
        ad_message_id=message.message_id,
        ad_chat_id=message.chat.id
    )
    
    # Confirm
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yuborish", callback_data="confirm_send"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="confirm_cancel")
        ]
    ])
    
    await message.answer(
        "Post qabul qilindi. Yuborishni tasdiqlaysizmi?",
        reply_markup=keyboard
    )
    await state.set_state(AdminStates.confirm_ad)

@router.callback_query(F.data == "confirm_cancel", AdminStates.confirm_ad)
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Yuborish bekor qilindi.")
    await callback.message.answer("Admin menyu:", reply_markup=get_admin_keyboard())

@router.callback_query(F.data == "confirm_send", AdminStates.confirm_ad)
async def start_broadcast(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    ad_msg_id = data['ad_message_id']
    ad_chat_id = data['ad_chat_id']
    await state.clear()
    
    await callback.message.edit_text("🚀 Xabar yuborish boshlandi...")
    
    users = get_all_users()
    groups = get_all_groups()
    targets = set(users + groups) # Unique IDs
    
    total = len(targets)
    sent = 0
    failed = 0
    
    if total == 0:
        await callback.message.edit_text("⚠️ Yuborish uchun foydalanuvchilar topilmadi (yangi baza bo'sh).")
        return

    progress_msg = await callback.message.answer(f"📤 Yuborilmoqda... 0/{total}")
    
    for i, chat_id in enumerate(targets):
        try:
            await bot.copy_message(
                chat_id=chat_id,
                from_chat_id=ad_chat_id,
                message_id=ad_msg_id
            )
            sent += 1
        except TelegramForbiddenError:
            # Bot blocked or kicked
            failed += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            try:
                await bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=ad_chat_id,
                    message_id=ad_msg_id
                )
                sent += 1
            except:
                failed += 1
        except Exception as e:
            logger.error(f"Broadcast error for {chat_id}: {e}")
            failed += 1
            
        # UI update every 10 users
        if i % 10 == 0:
            try:
                await progress_msg.edit_text(f"📤 Yuborilmoqda... {i+1}/{total}")
            except:
                pass
        
        # Rate limit safety
        await asyncio.sleep(0.05) 
        
    await progress_msg.delete()
    await callback.message.answer(
        f"✅ <b>Reklama yuborildi!</b>\n\n"
        f"Jami: {total}\n"
        f"Yuborildi: {sent}\n"
        f"Yetib bormadi (blok): {failed}",
        parse_mode="HTML",
        reply_markup=get_admin_keyboard()
    )
