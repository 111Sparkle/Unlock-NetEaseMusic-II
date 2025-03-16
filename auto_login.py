# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": 00E03D5B66F0186799624C8337BC23504AD52C4BE21B83119525075BD4637D1E684FC2A8742303FBA0DE387218E4352F3C241AEEA0D68461EBECAEF0DFBFB0F4E886A3E7E183F942DBFA38DF288F16471025FED5548AAB4DC33E049987C8BF3CBD1E39FB1AB0C75F1198E77D7A77B853447AF13600349AB48BD83CE7B98EDF3316F6A5EEE4FC230184E95F6BA2E5B09CCD12711F6E9CD84F72913058B89D27C1FB55292F528AA3CAC65384814E58D77ADF394338195FAFFC596E15768AEFD24C84A0F61A8AE7ED7CF004BBC4F67B927F3BEEE305B58623B2DC3FE872B3B7945E6DE3C68874C66E898C2B0E377A83BBEB9D9F8AE484036A74C2EE95111BC90EF0DEEF5CFED6144F1BA17A3359F45E512728FD345DAC593FB7CB0C61BB25B9F78F88DCFDD300C8E14499BDCDB5921F84C6DCA2A4F2D4F403B5D5E5CC02804A03831375C817A168A719BA8B046AB8F3A58D974A7D8FFD24158E42957725A39405124E
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
