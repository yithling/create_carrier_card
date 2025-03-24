
from bot.config import (
    MOSREG_CAR_LICENSE_URL,
    MOSREG_CARIER_LICENSE_URL,
    QR_FILE_PATH,
    MOSRU_CAR_LICENSE_URL,
    MOSRU_CARIER_LICENSE_URL,
    CAPTCHA_FILE_PATH,
    OSGOP_CHECK_URL,
    CARD_FILE_PATH
)

from bot.services import get_file_data, get_mosreg_license, get_mosru_license, get_osgop_data
from bot.utils import data_analysis, draw_card


#Получаем данные по лицензии из mosreg
def get_mosreg_license_data(driver, car_number) -> dict | None:
    try:
        #Получаем URL
        mosreg_car_url = MOSREG_CAR_LICENSE_URL.format(car_number)
        #Получаем данные по лицензии на машину
        mosreg_car_license = get_mosreg_license.CarLicense(driver, mosreg_car_url)
        mosreg_car_license_data = mosreg_car_license.extract_license_data()
        #Проверяем, есть ли данные
        if mosreg_car_license_data != {}:
            #Получаем URL на основе ИНН
            mosreg_carrier_url = MOSREG_CARIER_LICENSE_URL.format(
                mosreg_car_license_data["ИНН:"]
            )
            #Получаем данные по лицензии перевозчика
            mosreg_carrier_license = get_mosreg_license.CarierLicense(
                driver,
                mosreg_carrier_url,
                QR_FILE_PATH
            )
            mosreg_carrier_license_data = mosreg_carrier_license.extract_license_data()

            #Анализируем и формируем итоговый результат
            return data_analysis.merge_dict_mosreg(
                mosreg_car_license_data, mosreg_carrier_license_data
            )
        #Если данных нет, возвращаем None
        return None
    except:
        #Если произошла ошибка, возвращаем None
        return None



#Получаем данные по лицензии из mosru
def get_mosru_license_data(driver, car_number) -> dict | None:
    try:
        #Получаем URL
        mosru_car_url = MOSRU_CAR_LICENSE_URL
        #Получаем данные по лицензии на машину
        mosru_car_license = get_mosru_license.CarLicense(
            driver,
            mosru_car_url,
            car_number,
            CAPTCHA_FILE_PATH
        )
        mosru_car_license_data = mosru_car_license.extract_license_data()
        #Проверяем, есть ли данные
        if mosru_car_license_data != {}:
            #Получаем URL
            mosru_carier_url = MOSRU_CARIER_LICENSE_URL
            #Получаем данные по лицензии перевозчика
            mosru_carrier_license = get_mosru_license.CarierLicense(
                driver,
                mosru_carier_url,
                car_number,
                CAPTCHA_FILE_PATH
            )
            mosru_carrier_license_data = mosru_carrier_license.extract_license_data()

            #Если данные по лицензии перевозчика есть
            if mosru_carrier_license_data != {}:
            #Анализируем и формируем итоговый результат
                return data_analysis.merge_dict_mosru(
                    mosru_car_license_data,
                    mosru_carrier_license_data
                )
        #Если данных нет, возвращаем None
        return None
    except:
        #Если произошла ошибка, возвращаем None
        return None



def get_license_data(driver, car_number, region) -> dict | None:
    #Пытаемся получить данные по лицензии 3 раза
    for _ in range(3):
        #Проверяем по региону где искать лицензию, и получаем всю информацию по лицензии
        if region == "МО" or region == "MO":
            mosreg_data = get_mosreg_license_data(driver, car_number)
            if mosreg_data != {}:
                return mosreg_data

        if region == "МСК" or region == "MCK":
            mosru_data = get_mosru_license_data(driver, car_number)
            if mosru_data != {}:
                return mosru_data
    #Если не удалось получить данные, возвращаем None
    return None


#Создаем карточку
def create_card(driver, file_path, mode) -> str | None:
    #Получаем данные из файла
    file_data = get_file_data.parse_excel_file(file_path)
    #Проверяем, есть ли данные
    if file_data is not None:
        #Получаем нужные данные для карточки
        organization_name = file_data["Название организации"].strip()
        driver_name = file_data["Имя водителя"].strip()
        car_number = file_data["Номер машины"].strip()
        legal_address = file_data["Адрес организации"].strip()
        phone_number = file_data["Номер телефона"].strip()
        region = file_data["Регион"].strip().upper()

        #Получаем данные по лицензии
        license_data = get_license_data(
            driver,
            car_number,
            region
            )

        #Если данных по лицензии нет
        if license_data is not None:
            #Проверяем, какую карточку создавать

            #Если без указания ОСГОПа
            if mode == 0:
                osgop_data = None
                if region == "МО" or region == "MO":
                    return draw_card.build_mo_card(
                        organization_name,
                        driver_name,
                        phone_number,
                        car_number,
                        legal_address,
                        license_data,
                        osgop_data,
                        CARD_FILE_PATH.format("mo_card"),
                    )

                if region == "МСК" or region == "MCK":
                    return draw_card.build_msk_card(
                        organization_name,
                        driver_name,
                        phone_number,
                        car_number,
                        legal_address,
                        license_data,
                        osgop_data,
                    CARD_FILE_PATH.format("msk_card")
                    )

            #Если с указанием ОСГОПА  
            if mode == 1:
                #Пытаемся получить данные по ОСГОПу 3 раза
                osgop_data = None
                for _ in range(3):
                    #Получаем данные по ОСГОПу
                    osgop = get_osgop_data.OsgopInfo(
                        driver,
                        car_number,
                        OSGOP_CHECK_URL
                    )
                    osgop_data = osgop.extract_osgop_data()

                    if osgop_data is not None:
                        if region == "МО" or region == "MO":
                            return draw_card.build_mo_card(
                                organization_name,
                                driver_name,
                                phone_number,
                                car_number,
                                legal_address,
                                license_data,
                                osgop_data,
                                CARD_FILE_PATH.format("mo_osgop"),
                            )

                        if region == "МСК" or region == "MCK":
                            return draw_card.build_msk_card(
                                organization_name,
                                driver_name,
                                phone_number,
                                car_number,
                                legal_address,
                                license_data,
                                osgop_data,
                                CARD_FILE_PATH.format("msk_osgop")
                            )

                #Если не удалось получить данные по ОСГОПу, то делаем карточку без данных
                if region == "МО" or region == "MO":
                    return draw_card.build_mo_card(
                        organization_name,
                        driver_name,
                        phone_number,
                        car_number,
                        legal_address,
                        license_data,
                        osgop_data,
                        CARD_FILE_PATH.format("mo_osgop"),
                        )

                if region == "МСК" or region == "MCK":
                    return draw_card.build_msk_card(
                        organization_name,
                        driver_name,
                        phone_number,
                        car_number,
                        legal_address,
                        license_data,
                        osgop_data,
                        CARD_FILE_PATH.format("msk_osgop")
                        )
        #Если не удалось получить данные по лицензии, возвращаем None
        else:
            return None 

    #Если не удалось получить данные из файла, возвращаем None 
    else:
        return None
