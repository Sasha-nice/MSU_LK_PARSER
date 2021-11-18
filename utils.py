from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
grades_dict = {
    'удов.': 3,
    'хорошо': 4,
    'отлично': 5,
    'зачтено': 'зачтено'
}


def in_diploma(grade):
    try:
        grade.find_element(By.CLASS_NAME, 'text-success')
        return True
    except WebDriverException:
        return False


def get_name(grade):
    try:
        return grade.find_element(By.CLASS_NAME, 'text-success').text
    except WebDriverException:
        return grade.find_elements(By.TAG_NAME, 'td')[1].text.split('\n')[0]


def options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return chrome_options
