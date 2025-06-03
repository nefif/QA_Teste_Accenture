from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ProgressBarPage:
    def __init__(self, driver):
        self.driver = driver
        self.start_stop_reset_button_id = "startStopButton"
        self.progress_bar_id = "progressBar"
        self.progress_bar_value_selector = (By.CSS_SELECTOR, f"#{self.progress_bar_id} > div")


    def click_start_stop_reset_button(self):
        """Clica no botão Start/Stop/Reset."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.start_stop_reset_button_id))
        ).click()

    def get_progress_bar_value(self):
        """Retorna o valor atual da barra de progresso como um inteiro."""
        try:
            progress_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.progress_bar_value_selector)
            )
            value_text = progress_element.get_attribute("aria-valuenow")
            if value_text is None: 
                 value_text = progress_element.text.replace('%', '')
            
            if value_text:
                return int(value_text)
            return 0 
        except:
            return 0 

    def stop_progress_before_value(self, target_value_str):
        """Clica em Start e depois em Stop quando o valor da barra estiver próximo, mas antes do target_value."""
        target_value = int(target_value_str.replace('%', ''))
        
        # Clica em Start se o botão estiver como "Start"
        button_text = self.driver.find_element(By.ID, self.start_stop_reset_button_id).text
        if button_text.lower() == "start":
            self.click_start_stop_reset_button()

        for _ in range(20):
            current_value = self.get_progress_bar_value()

            if current_value > 0 and current_value >= (target_value - 5): 
                 if current_value < target_value :
                    self.click_start_stop_reset_button() 
                    print(f"DEBUG: Barra parada em {current_value}% (alvo < {target_value}%)")
                    return True
            if current_value >= target_value: 
                self.click_start_stop_reset_button() 
                print(f"DEBUG: Barra parada em {current_value}% (alvo era < {target_value}%, mas passou)")
                return False 
            time.sleep(0.1) 
        

        self.click_start_stop_reset_button() 
        print(f"DEBUG: Timeout ao tentar parar antes de {target_value}%. Parado em {self.get_progress_bar_value()}%.")
        return False


    def wait_for_progress_to_reach_value(self, target_value_str):
        """Espera até que a barra de progresso atinja o valor especificado."""
        target_value = int(target_value_str.replace('%', ''))

        try:
            WebDriverWait(self.driver, 30).until( 
                lambda driver: self.get_progress_bar_value() >= target_value
            )
            print(f"DEBUG: Barra atingiu {self.get_progress_bar_value()}% (alvo era {target_value}%)")
        except Exception as e:
            print(f"DEBUG: Timeout esperando a barra atingir {target_value}%. Valor atual: {self.get_progress_bar_value()}%. Erro: {e}")

            pass


    def get_button_text(self):
        """Retorna o texto atual do botão Start/Stop/Reset."""
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.start_stop_reset_button_id))
        ).text