import csv

from pageTest import pageTest
from time import sleep
from selenium.common.exceptions import TimeoutException

class pageScroll(pageTest):
    def do_scrool_test(self):
        for url in self._get_scroll_url():
            self._scroll_page(url)

        self._save_error_log()

        self.driver.close()
        self.mobile_driver.close()

    def _get_scroll_url(self):
        urls = []
        with open('csv/scroll_url.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                urls.append(row[0])
        return urls

    def _scroll_page(self, url):
        if 'sp' in url:
            driver = self.mobile_driver
        else:
            driver = self.driver

        try:
            self._navigate_to_url(driver, url)
        except TimeoutException as e:
            self._append_error_logs(url, 'Scroll TimeoutException')
            return

        SCROLL_PAUSE_TIME = 0.1
        SCROLL_ONCE = 200
        new_height = 0
        last_height = driver.execute_script("return document.body.scrollHeight") - SCROLL_ONCE

        while True:
            next_height = new_height + SCROLL_ONCE
            driver.execute_script("window.scrollTo(" + str(new_height) + ", " + str(next_height) + ");")

            sleep(SCROLL_PAUSE_TIME)
            if new_height > last_height:
                break
            new_height = next_height

pageScroll().do_scrool_test()
