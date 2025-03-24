from aiogram import Router
from aiogram.types import Message
from aiogram.types.file import File
from aiogram.filters import Command


router = Router()


@router.message(Command("help"))
async def help_command(msg: Message):
    await msg.answer("""
/start - Включить бот
/osgop_carrier_card - Получить карточку перевозчика с ОСГОП.
/carrier_card - Получить карточку перевозчика без ОСГОП.
                     """)