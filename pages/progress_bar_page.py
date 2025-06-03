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
            # O valor está no atributo 'aria-valuenow' ou no texto da div interna
            value_text = progress_element.get_attribute("aria-valuenow")
            if value_text is None: # Fallback para o texto, se aria-valuenow não estiver presente ou for None
                 value_text = progress_element.text.replace('%', '')
            
            if value_text:
                return int(value_text)
            return 0 # Retorna 0 se não conseguir extrair o valor
        except:
            return 0 # Em caso de erro ao encontrar o elemento ou valor

    def stop_progress_before_value(self, target_value_str):
        """Clica em Start e depois em Stop quando o valor da barra estiver próximo, mas antes do target_value."""
        target_value = int(target_value_str.replace('%', ''))
        
        # Clica em Start se o botão estiver como "Start"
        button_text = self.driver.find_element(By.ID, self.start_stop_reset_button_id).text
        if button_text.lower() == "start":
            self.click_start_stop_reset_button()

        # Monitora o progresso e clica em Stop
        # Tentativas para garantir que o valor seja lido após o início do progresso
        for _ in range(20): # Tenta por até 2 segundos (20 * 0.1s)
            current_value = self.get_progress_bar_value()
            # Adiciona uma pequena margem para clicar em stop um pouco antes.
            # Se o valor for 0 no início, espera um pouco para o progresso começar.
            if current_value > 0 and current_value >= (target_value - 5): # Ex: se target é 25, para em 20 ou mais
                 if current_value < target_value : # Garante que não passou
                    self.click_start_stop_reset_button() # Clica em Stop
                    print(f"DEBUG: Barra parada em {current_value}% (alvo < {target_value}%)")
                    return True
            if current_value >= target_value: # Se já passou ou atingiu, para e indica que não conseguiu parar antes.
                self.click_start_stop_reset_button() # Clica em Stop
                print(f"DEBUG: Barra parada em {current_value}% (alvo era < {target_value}%, mas passou)")
                return False # Indica que não conseguiu parar antes
            time.sleep(0.1) # Pequena pausa para não sobrecarregar e permitir atualização do DOM
        
        # Se o loop terminar e não parou (ex: progresso muito lento ou muito rápido)
        self.click_start_stop_reset_button() # Tenta parar de qualquer forma
        print(f"DEBUG: Timeout ao tentar parar antes de {target_value}%. Parado em {self.get_progress_bar_value()}%.")
        return False


    def wait_for_progress_to_reach_value(self, target_value_str):
        """Espera até que a barra de progresso atinja o valor especificado."""
        target_value = int(target_value_str.replace('%', ''))
        # Usa WebDriverWait para esperar que o atributo 'aria-valuenow' atinja o valor
        # Ou que o texto da barra de progresso seja o valor esperado
        try:
            WebDriverWait(self.driver, 30).until( # Timeout maior para 100%
                lambda driver: self.get_progress_bar_value() >= target_value
            )
            print(f"DEBUG: Barra atingiu {self.get_progress_bar_value()}% (alvo era {target_value}%)")
        except Exception as e:
            print(f"DEBUG: Timeout esperando a barra atingir {target_value}%. Valor atual: {self.get_progress_bar_value()}%. Erro: {e}")
            # Considerar levantar uma exceção aqui se o comportamento desejado for falhar o teste
            pass


    def get_button_text(self):
        """Retorna o texto atual do botão Start/Stop/Reset."""
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.start_stop_reset_button_id))
        ).text