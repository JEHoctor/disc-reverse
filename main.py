from time import sleep
from typing import List, Tuple

import pandas as pd
import typer
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

disc_test_url = "https://www.123test.com/disc-personality-test/index.php"


class QuestionGroup:
    def __init__(self, driver: WebDriver, table: WebElement) -> None:
        self.driver = driver
        self.rows = table.find_elements(By.TAG_NAME, "tr")

    def get_descriptions(self) -> List[str]:
        return [row.text for row in self.rows]

    def _get_thumbs(self, row_index: int) -> Tuple[WebElement, WebElement]:
        row = self.rows[row_index]
        thumbs_up, thumbs_down = row.find_elements(By.TAG_NAME, "img")
        return thumbs_up, thumbs_down

    def select_up(self, up: int) -> None:
        thumbs_up, thumbs_down = self._get_thumbs(row_index=up)
        sleep(1)
        self.driver.execute_script("arguments[0].click()", thumbs_up)

    def select_down(self, down: int) -> None:
        thumbs_up, thumbs_down = self._get_thumbs(row_index=down)
        sleep(1)
        self.driver.execute_script("arguments[0].click()", thumbs_down)

def take_quiz(driver: WebDriver) -> None:
    sleep(1)
    driver.get(disc_test_url)
    sleep(3)

    tables = driver.find_elements(By.TAG_NAME, "table")
    for table in tables:
        question_group = QuestionGroup(driver, table)
        question_group.select_up(0)
        question_group.select_down(1)

    (submit_button,) = (b for b in driver.find_elements(By.TAG_NAME, "button") if b.text == "Next")
    sleep(1)
    driver.execute_script("arguments[0].click()", submit_button)

def main() -> WebDriver:
    driver = webdriver.Firefox()
    take_quiz(driver)
    return driver

if __name__ == "__main__":
    typer.run(main)
