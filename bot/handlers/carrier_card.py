import os

from aiogram import Bot, F, Router
from aiogram.types import (Message, FSInputFile)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


from bot.config import EXCEL_FILE_PATH
from bot.utils import create_carrier_card

router = Router()

#Создаем класс для состояний
class CarrierCardMode(StatesGroup):
    mode = State()

#Если заказана карточка перевозчика без ОСГОП
@router.message(Command("carrier_card"))
async def create_osgop_carrier_card(msg: Message, state: FSMContext):
    await state.set_state(CarrierCardMode.mode)
    #Устанавливаем режим
    await state.update_data(mode=0)
    await msg.answer("Загрузите Excel File")


#Скачиваем файл и создаем карточку без ОСГОП
@router.message(F.document, CarrierCardMode.mode)
async def download_file(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    if not msg.document:
        await msg.answer("Вы не загрузили документ.")
        return
    
    #Проверяем расширение файла
    file_name = msg.document.file_name
    if file_name is not None and not file_name.endswith(".xlsm"):
        await msg.answer("Пожалуйста загрузите файл с разрешение xlsm")
        return

    #Получаем id файла
    file_id = msg.document.file_id
    #Пытаемся скачать файл
    try:
        #Скачиваем файл
        file = await bot.get_file(file_id)
        file_path = file.file_path
        if not file_path:
            await msg.answer("Проихошла ошибка, не могу загрузить файл!")
            return

        #Путь для сохранения файла
        download_path = EXCEL_FILE_PATH.format(user_id, file_name)

        #Узнаем тип карточки
        get_mode = await state.get_data()
        await state.clear()

        #Скачиваем документ
        await bot.download_file(file_path, download_path)
        await msg.answer("Файл загружен, ожидайте!")

        #Создаем firefox браузер Selenium
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

        #Делаем карточку
        mode = get_mode["mode"]
        carrier_card_path = create_carrier_card.create_card(driver, download_path, mode)
        #Если карточка создана, отправляем ее в бот
        if carrier_card_path is not None:
            await msg.answer("Карточка готова! Проверьте перед печатью!")
            card = FSInputFile(carrier_card_path)
            await msg.answer_document(card)
            os.remove(download_path)
            os.remove(carrier_card_path)
        else:
            await msg.answer("Ошибка, проверьте файл с путевым.")
 
        #Завершаем работу браузера и удаляем файлы
        driver.quit()
    #Если произошла ошибка, отправляем ошибку в бот
    except Exception as e:
        await msg.answer(f"Не удалось скачать, ошибка - {e}")
