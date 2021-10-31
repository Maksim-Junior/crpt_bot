from BaseApp import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class Locators:
    LINK_COUNT_TABLE = (By.XPATH, '//*[@id="table_maina"]/tbody')

class Helper(Base):
    def find_count(self):
        return self.find_element(Locators.LINK_COUNT_TABLE, time=10)

