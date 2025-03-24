def merge_dict_mosreg(car_license_dict, carrier_license_dict) -> dict | None:
    #Анализируем, удаляем лишние и получаем нужный словарь по данным из лицензии Московской области
    data_frame = {
        "Статус:": "",
        "Перевозчик (наименование ЮЛ или ИП):": "",
        "Государственный регистрационный номер:": "",
        "Номер реестровой записи в региональном реестре легкового такси:": "",
        "Номер реестровой записи в региональном реестре перевозчиков легковым такси:": "",
        "Дата предоставления разрешения:": "",
        "Срок действия разрешения:": "",
        }

    if car_license_dict != {} and carrier_license_dict != {}:
        #Чекаем, привязана ли лицензия 
        check_status = car_license_dict.pop("Внесено в разрешение перевозчика:").strip()
        if car_license_dict["Статус:"].strip() == "Действующее" and carrier_license_dict["Статус:"].strip() == "Действующее":
            if check_status.isdigit():
                for key, value in car_license_dict.items():
                    if key.strip() in data_frame and key != "Статус:":
                        data_frame[key] = value.strip()
                for key, value in carrier_license_dict.items():
                    if key.strip() in data_frame and key != "Статус:":
                        data_frame[key] = value.strip()
        return data_frame

    return None


def merge_dict_mosru(car_license_dict, carrier_license_dict) -> dict | None:
    #Анализируем, удаляем лишние и получаем нужный словарь по данным из лицензии Москвы
    data_frame = {
        "Статус": "",
        "Фамилия, Имя, Отчество индивидуального предпринимателя или физического лица": "",
        "Полное наименование юридического лица": "",
        "Государственный регистрационный номер транспортного средства": "",
        "Номер записи в региональном реестре легковых такси, содержащий сведения о легковом такси": "",
        "Номер записи в региональном реестре перевозчиков легковым такси, содержащий сведения о перевозчике": "",
        "Дата внесения записи в региональный реестр перевозчиков легковым такси": "",
        "Дата окончания срока действия разрешения": "",
    }

    if car_license_dict != {} and carrier_license_dict != {}:
        for key, value in car_license_dict.items():
            if key in data_frame:
                data_frame[key] = value
        for key, value in carrier_license_dict.items():
            if key in data_frame:
                data_frame[key] = value
        return data_frame
    else:
        return None

