from openpyxl import load_workbook


# Функция для парсинга файла
def parse_excel_file(file_path):
    #Загружаем файл, и сохраняем значение по номерам ячеек
    workbook = load_workbook(file_path, keep_vba=True)
    sheet = workbook.active

    if sheet is None:
        return None

    return {
            "Название организации": sheet["R7"].value,
            "Адрес организации": sheet["K8"].value,
            "Номер телефона": sheet["N9"].value.upper(),
            "Номер машины": sheet["AL11"].value,
            "Имя водителя": sheet["U12"].value,
            "Регион": sheet["BI14"].value.upper()

    }

