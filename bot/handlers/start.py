from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command("start"))
async def start_cmd(msg: Message):
    await msg.answer("""
/osgop_carrier_card - Получить карточку перевозчика с ОСГОП.
/carrier_card - Получить карточку перевозчика без ОСГОП.
                     """)

