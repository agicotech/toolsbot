import logging
import traceback

for i in range(3):
    try:
        import asyncio
        from aiogram import Bot, Dispatcher, F
        from aiogram.fsm.storage.memory import MemoryStorage
        from consts import BOT_TOKEN, BOT_NAME
        from aiogram.enums import ParseMode
        from aiogram.fsm.context import FSMContext
        from aiogram.fsm.storage.base import StorageKey
        import aiogram.exceptions as exceptions
        from aiogram.types import Message
        from aiogram.types.error_event import ErrorEvent
        from aiogram.filters import ExceptionTypeFilter
        import asyncio
        import common, tools_routes, postrouter
        break 
    except ModuleNotFoundError as mnf:
        logging.basicConfig(level='INFO')
        import os, sys, logging
        if i == 2:
            logging.warning(f'Unable to install requirements')
            exit(-1)
        logging.warning(f'Module not found: {mnf}')
        os.system(f'{sys.executable} -m pip install -r requirements.txt')

    except Exception as e:
        import logging
        logging.critical(e, exc_info=True)
        exit(-1)
logger = logging.getLogger(name=BOT_NAME)




async def main():

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(BOT_TOKEN)


    dp.include_router(common.router)
    dp.include_router(tools_routes.router)
    dp.include_router(postrouter.router)

    @dp.error(ExceptionTypeFilter(exceptions.AiogramError))
    def aioerror(event: ErrorEvent):
        logger.warning(f'Aiogram error',  {"error" : f'{type(event.exception)}:{event.exception}'})

    @dp.error(F.update.message.as_('message') |
               F.update.callback_query.message.as_('message'))
    async def error_handler(event: ErrorEvent, message: Message):
        try:
            logger.error("Global Exception", {"error" : f'{type(event.exception)}:{event.exception}'})
            logger.error(event.exception, exc_info=True)
            await message.answer('Случилась ошибка')
        except:
            pass
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logger.info('Startup')
    asyncio.run(main())