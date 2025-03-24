import os
from dotenv import load_dotenv

load_dotenv()

#Токены
BOT_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
CAPTCHA_TOKEN = os.getenv("CAPTCHA_API_TOKEN")

#Расположение файлов
CAPTCHA_FILE_PATH = "./bot/media/downloads/captcha.png"
QR_FILE_PATH = "./bot/media/downloads/qr.png"
EXCEL_FILE_PATH = "./bot/media/uploads/{}_{}"
CARD_FILE_PATH = "./bot/media/tables/{}.docx"
RESULT_FILE_PATH = "./bot/media/card_result/{}-{}.docx"
LOG_FILE = "./log.log"

#Ссылки
MOSREG_CAR_LICENSE_URL = "https://mtdi.mosreg.ru/taxi-cars?licenseNumber=&inn=&name=&gosNumber={}&region=ALL"
MOSREG_CARIER_LICENSE_URL = "https://mtdi.mosreg.ru/taxi-permits?licenseNumber=&inn={}&name=&region=ALL"
MOSRU_CAR_LICENSE_URL = "https://transport.mos.ru/auto/reestr_taxi"
MOSRU_CARIER_LICENSE_URL = "https://transport.mos.ru/auto/reestr_carrier"
OSGOP_CHECK_URL = "https://nsso.ru/check_policy/gop/tsnumber/"
