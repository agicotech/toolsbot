from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
import logging
logger = logging.getLogger(name='DEMOT-BOT')


router = Router()



@router.message(Command('start', 'начать'))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
"""
Привет!👋🏿
Этот бот позволяет немного упростить жизнь программиста)
Он умеет:
- ✍🏻 Форматировать Markdown в нормальное телеграм сообщение
- 👨‍💻 Преобразовывать curl запрос в requests
"""
    )

@router.callback_query(F.data == 'SuperExit')
async def delexit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.clear()
