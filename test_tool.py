from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

class TestTool:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def set_driver_url(self, url):
        self.driver.get(url)

    def close_driver(self):
        self.driver.close()

    def require_test(self, xpath, input):
        element = self.driver.find_element_by_xpath(xpath)
        element_parent = self.driver.find_element_by_xpath(xpath + "/parent::div")

        element.send_keys(input)
        element.send_keys(Keys.TAB);
        self.__assert_equal("successInput", element_parent.get_attribute("class"))

        element.send_keys(Keys.BACK_SPACE * 20)
        element.send_keys(Keys.TAB);
        self.__assert_equal("noDataInput", element.get_attribute("class"))

        element.send_keys(input)
        element.send_keys(Keys.TAB);

    def hide_symfony_toolbar(self):
        try:
            hide_button = self.driver.find_element_by_xpath("//div[@class='sf-toolbar']//a[@class='hide-button']")
            hide_button.click()
        except:
            pass

    def __assert_equal(self, expect, input):
        assert input == expect, 'expect[{0}], input[{1}]'.format(expect, input)
