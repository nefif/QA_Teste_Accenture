# pages/home_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com"

    def abrir(self):
        self.driver.get(self.url)

    def clicar_menu_forms(self):
        """
        Clica no card 'Forms' na página inicial.
        """
        elemento = self.driver.find_element(By.XPATH, "//h5[text()='Forms']/ancestor::div[@class='card mt-4 top-card']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        elemento.click()

    def clicar_practice_form(self):
        """
        Clica na opção 'Practice Form' no menu lateral.
        """
        elemento = self.driver.find_element(By.XPATH, "//span[text()='Practice Form']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        elemento.click()
