import ssl
import csv

from retry import retry
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

class pageTest:
    def __init__(self):
        self.error_logs = []

        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)

        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'browser': 'SEVERE'}

        self.driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=caps)
        self.driver.set_page_load_timeout(5)

        mobile_emulation = { "deviceName": "iPhone 6" }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.mobile_driver = webdriver.Chrome(chrome_options=chrome_options)
        self.mobile_driver.set_page_load_timeout(5)

        # HTTPS対応
        ssl._create_default_https_context = ssl._create_unverified_context

    def _save_error_log(self):
        with open('csv/result.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(self.error_logs)

    @retry(TimeoutException, tries=3, delay=1)
    def _navigate_to_url(self, driver, url):
        if '.xml' in url:
            return
        driver.get(url)

    def _append_error_logs(self, url, message):
        print(url, message)
        self.error_logs.append([url, message])
