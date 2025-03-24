import time

from bs4 import BeautifulSoup as bs
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.by import By

from bot.config import CAPTCHA_TOKEN


class OsgopInfo:
    #Получаем данные по ОСГОП
    def __init__(self, driver, car_number, url):
        self.car_number = car_number
        self.driver = driver
        self.url = url
        self.driver.get(self.url)
        self.page_source = self.get_source_page()


    def solve_captcha(self):
        #Берем sitekey google капчи и отправляем на решение
        solver = TwoCaptcha(CAPTCHA_TOKEN)
        try:
            result = solver.recaptcha(
                sitekey="6LfrBeEUAAAAAPQZbP7JJe63BSzH3zO9jFv2atLv",
                url=self.url,
                version="3"
            )
        except Exception:
            return ""
        return result


    def get_source_page(self) -> str | None:
        #Получаем данные по странице

        #Убираем галочку для получения всех страховок ОСГОП
        try:
            checkbox = self.driver.find_element(By.ID, "show_contracts_by_date")
            if checkbox.is_selected():
                checkbox.click()
            #Указываем номер машины который мы ищем
            carnumber_form = self.driver.find_element(By.ID, "sDocNo_TS")
            carnumber_form.send_keys(self.car_number.strip())
            #Решаем re-captcha
            captcha_solution = self.solve_captcha()['code']
            
            #recaptcha_response_element = self.driver.find_element(By.ID, "g-recaptcha-response")
            self.driver.execute_script(
                f'document.getElementById("g-recaptcha-response").innerHTML="{captcha_solution}";'
            )

            search_button = self.driver.find_element(By.NAME, "SUBMIT_CheckInsuranceFactForm")
            search_button.click()
            time.sleep(7)
            return self.driver.page_source
        except:
            return None

    def extract_osgop_data(self) -> dict | None:
        #Возвращаем данные по лицензии
        html_page = None
        for _ in range(3):
            html_page = self.page_source
            if html_page != None:
                osgop_data = {}
                soup = bs(html_page, "lxml")
                result_message_sub = soup.find("div", {"class": "result_message_sub"})
                if result_message_sub != None:
                    result = result_message_sub.get_text(separator="\n")
                    records = []
                    for data in result.split(",")[:3]:
                        records.append(data)

                    for record in records:
                        record = record.lstrip()
                        record = record.split(":")
                        key, value = record[0], record[1]
                        if "№" in key:
                            key = key.split("№", 1)[-1]
                            key = "№" + key
                        osgop_data[key] = osgop_data.get(key, value)
                    return osgop_data

        return None
