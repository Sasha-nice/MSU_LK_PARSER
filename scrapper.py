from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from statistics import mean
from utils import grades_dict, in_diploma, get_name, options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


class MsuParser:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.start_url = 'https://lk.msu.ru/site/login'
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options())

    def get_grades(self):
        self.driver.get(self.start_url)

        login_form = self.driver.find_element(By.ID, 'loginform-email')
        login_form.click()
        login_form.send_keys(self.email)

        password_form = self.driver.find_element(By.ID, 'loginform-password')
        password_form.click()
        password_form.send_keys(self.password)

        login_button = self.driver.find_element(By.NAME, 'login-button')
        login_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/ul/li[3]'))
            ).click()

        return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/table/tbody'))
                ).find_elements(By.TAG_NAME, 'tr')

    def get_grades_lists(self):
        grades_list = [{
            'sem': int(grade.find_element(By.CLASS_NAME, 'grid-label-postfix').text),
            'name': get_name(grade),
            'grade': grades_dict[grade.find_element(By.CLASS_NAME, 'bold-if-mobile').text],
            'diplom': in_diploma(grade)}
            for grade in self.grades
            if grade.find_element(By.CLASS_NAME, 'bold-if-mobile').text != 'зачтено']

        return grades_list

    def get_mean_grades(self):
        max_semestr = max([i['sem'] for i in self.grades_list])
        with open('grades.txt', 'w') as f:
            for semestr in range(1, max_semestr + 1):
                f.write(
                    f'Средний балл к концу {semestr} семестра:' +
                    "{0:.2f}".format(mean([i["grade"] for i in self.grades_list
                                           if i["sem"] in list(range(1, semestr + 1))])) +
                    '\n')
                f.write(
                    f'Средний балл к концу {semestr} семестра в диплом: ' +
                    "{0:.2f}".format(mean([i["grade"] for i in self.grades_list
                                           if (i["sem"] in list(range(1, semestr + 1)) and i["diplom"])])) +
                    '\n')

    def get_csv(self):
        df = pd.DataFrame(self.grades_list)
        df.to_csv('grades.csv', encoding='utf-8', index=False)

    def start(self):
        self.grades = self.get_grades()
        self.grades_list = self.get_grades_lists()
        self.get_mean_grades()
        self.get_csv()
        self.driver.quit()
