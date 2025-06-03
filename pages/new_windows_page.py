from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewWindowsPage:
    def __init__(self, driver):
        self.driver = driver
        self.new_window_button_id = "windowButton"
        self.sample_heading_id = "sampleHeading" 

    def clicar_new_window_button(self):
        """Clica no botão 'New Window'."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.new_window_button_id))
        ).click()

    def verificar_mensagem_nova_janela(self, mensagem_esperada):
        """
        Muda para a nova janela, verifica a mensagem e retorna o handle da janela original.
        """
        original_window_handle = self.driver.current_window_handle
        all_window_handles = self.driver.window_handles

        new_window_handle = None
        for handle in all_window_handles:
            if handle != original_window_handle:
                new_window_handle = handle
                break
        
        if not new_window_handle:
            return False, original_window_handle 

        self.driver.switch_to.window(new_window_handle)
        
        try:

            mensagem_elemento = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, self.sample_heading_id))
            )
            mensagem_encontrada = mensagem_elemento.text
            print(f"DEBUG: Texto encontrado na nova janela: '{mensagem_encontrada}'") 
            return mensagem_esperada in mensagem_encontrada, original_window_handle
        except Exception as e:
            print(f"DEBUG: Erro ao verificar mensagem na nova janela: {e}") 
            return False, original_window_handle 
        finally:
            pass

    def fechar_janela_atual_e_retornar_para_original(self, original_window_handle):
        """Fecha a janela atual (que deve ser a nova) e retorna para a janela original."""
        if self.driver.current_window_handle != original_window_handle:
            self.driver.close() 
        self.driver.switch_to.window(original_window_handle)

    def verificar_retorno_janela_original(self, original_window_handle):
        """Verifica se o foco retornou para a janela original."""
        return self.driver.current_window_handle == original_window_handle