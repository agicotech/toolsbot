from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InputMediaPhoto
from aiogram.enums import ParseMode
import json
import time
from datetime import datetime
from aiogram.types import BufferedInputFile,  ReactionTypeEmoji
from consts import REACTION_OK, BOT_NAME
from aiogram.fsm.context import FSMContext
import random
import asyncio
from simple_row import *
from tools.curl2requests import curl2requests
from tools.md2tg import markdown_to_html
import os, logging
logger = logging.getLogger(name=BOT_NAME)

router = Router()

@router.message(F.text.strip().lower().startswith('curl'))
async def process_curl(message: Message):
    await message.react(REACTION_OK)
    answer = \
f"""**🐍 Here's your python request**:

```python
{curl2requests(message.text)}
```
"""
    await message.reply(answer, parse_mode=ParseMode.MARKDOWN_V2)

@router.message(F.text)
async def process_md(message: Message):
    await message.react(REACTION_OK)
    await message.answer(markdown_to_html(message.html_text), parse_mode=ParseMode.HTML)