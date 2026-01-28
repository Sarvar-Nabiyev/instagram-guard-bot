"""
Guruh a'zoligi handler
Bot guruhga qo'shilgan/chiqarilgan paytda statistikani yangilaydi.
"""

from aiogram import Router
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from services.stats import track_group

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def bot_added_to_group(event: ChatMemberUpdated):
    """Bot guruhga qo'shilganda"""
    chat_id = event.chat.id
    # Faqat guruhlar uchun (supergroup yoki group)
    if event.chat.type in ('group', 'supergroup'):
        track_group(chat_id, joined=True)


@router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def bot_removed_from_group(event: ChatMemberUpdated):
    """Bot guruhdan chiqarilganda"""
    chat_id = event.chat.id
    if event.chat.type in ('group', 'supergroup'):
        track_group(chat_id, joined=False)
