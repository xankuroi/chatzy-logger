from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import re
import time
import configparser

if os.listdir('logs/'):
    'Logs already exist!'

def filter_count(elems):
    return len(list(filter(lambda elem: re.match(r'\d{1,2}:\d{2} (A|P)M', elem.get_attribute('innerHTML')), elems)))

def scrape():
    config = configparser.ConfigParser()
    settings = config.read('config.ini')
    driver = None

    browser = settings['BROWSER']
    if browser == "Firefox":
        driver = webdriver.Firefox()
    elif browser == "Opera":
        driver = webdriver.Opera()
    else:
        driver = webdriver.Chrome()

    driver.get(settings['LINK'])
    driver.implicitly_wait(10)

    # Enter the room
    driver.find_element_by_id('X7126').send_keys(settings['NAME'], Keys.RETURN)

    # Go into Review Mode
    driver.find_element_by_id('X5662').click()

    # Navigate to the very beginning
    nums = driver.find_element_by_css_selector('#X4668 > p:nth-child(1) > a:nth-child(2) > b')
    curr = nums.get_attribute('innerHTML')
    nums.click()
    driver.execute_script('document.getElementById('X2785').scrollBy(-999999999, 0)', '')
    driver.find_element_by_id('X8637').click()

    time.sleep(1)
    count = 1
    logs = open(f'logs/logs_{count}.html', 'w+', encoding='utf-8')
    elements = driver.find_elements_by_class_name('X5359')

    # While you haven't seen a timestamp...
    while(filter_count(elements) == 0 and count < 25):
        # Make a new file for every 25 pages
        if(count % 25 == 0):
            print(count)
            logs.close()
            logs = open(f'logs/logs_{str(count).zfill(5)}.html', 'w+', encoding='utf-8')

        # Write to file
        logs.write(driver.find_element_by_id('X4668').get_attribute('innerHTML'))

        # Go to the next page
        driver.find_element_by_css_selector('#X4668 > p:nth-child(1) > a:nth-child(3) > span').click()
        WebDriverWait(driver, 10, poll_frequency=0.1).until(EC.staleness_of(elements[0]))

        elements = driver.find_elements_by_class_name('X5359')
        count += 1

    logs.close()
    driver.quit()
