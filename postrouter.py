from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from simple_row import inlbuttonblock
from consts import REACTION_UNKNOWN

router = Router()
stdmarkup = inlbuttonblock(['Меню'])


@router.callback_query()
async def error_callback(message: CallbackQuery, state: FSMContext):
    await message.answer('Ошибочное действие')


@router.message()
async def error_message(message: Message, state: FSMContext):
    await message.react(REACTION_UNKNOWN)
    
#@router.channel_post()
#async def channel_post(message: Message):
#    print(message)

