from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os

class CadastroPage:
    def __init__(self, driver):
        self.driver = driver

    def preencher_campos_principais(self):
        """
        Preenche todos os campos do formulário, exceto o upload de arquivo.
        """
        # firstName
        fn_element = self.driver.find_element(By.ID, "firstName")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fn_element)
        fn_element.send_keys("João")

        # lastName
        ln_element = self.driver.find_element(By.ID, "lastName")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ln_element)
        ln_element.send_keys("Silva")
        
        # userEmail
        email_element = self.driver.find_element(By.ID, "userEmail")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_element)
        email_element.send_keys("joao@email.com")
        
        # Gender (Male)
        gender_element = self.driver.find_element(By.XPATH, "//label[text()='Male']")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gender_element)
        gender_element.click()

        # Hobbies: "Reading"
        reading_hobby_locator = (By.XPATH, "//label[@for='hobbies-checkbox-2']")
        reading_hobby_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(reading_hobby_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reading_hobby_element)
        reading_hobby_element.click()

        # userNumber
        un_element = self.driver.find_element(By.ID, "userNumber")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", un_element)
        un_element.send_keys("11999999999")


        # Subjects: Escrever "Hindi" e selecionar
        subjects_input_locator = (By.ID, "subjectsInput")
        subjects_input_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(subjects_input_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", subjects_input_element)
        subjects_input_element.send_keys("Hindi")
        hindi_option_locator = (By.XPATH, "//div[contains(@class, 'subjects-auto-complete__option') and text()='Hindi']")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(hindi_option_locator)).click()
        
        # currentAddress
        ca_element = self.driver.find_element(By.ID,"currentAddress")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ca_element)
        ca_element.send_keys("Rua Teste") 

        # Select State (primeira opção)
        state_dropdown_locator = (By.ID, "state")
        state_dropdown_trigger_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(state_dropdown_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", state_dropdown_trigger_element)
        state_dropdown_trigger_element.click()
        first_state_option_locator = (By.ID, "react-select-3-option-0")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(first_state_option_locator)).click()

        # Select City (primeira opção)
        city_dropdown_locator = (By.ID, "city")
        city_dropdown_trigger_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(city_dropdown_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", city_dropdown_trigger_element)
        city_dropdown_trigger_element.click()
        first_city_option_locator = (By.ID, "react-select-4-option-0")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(first_city_option_locator)).click()

    def fazer_upload_arquivo(self):
        """
        Realiza o upload do arquivo especificado.
        """
        upload_file_locator = (By.ID, "uploadPicture")
        upload_file_input_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(upload_file_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_file_input_element)
        
        file_name = "Texto.txt"
        project_root = os.getcwd() # Assume que o behave é executado da raiz do projeto
        data_folder_path = os.path.join(project_root, "data")
        
        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)
        file_path = os.path.join(data_folder_path, file_name)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("Este é um arquivo de texto para o upload de teste.")
        
        upload_file_input_element.send_keys(file_path)

    def enviar_formulario(self):
        submit_button_locator = (By.ID, "submit")
        submit_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(submit_button_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(submit_button_locator)).click()

    def verificar_confirmacao(self):
        modal_title_locator = (By.ID, "example-modal-sizes-title-lg")
        
        # Espera o título do modal aparecer e pega o elemento
        modal_title_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(modal_title_locator)
        )
        
        modal_title_text = modal_title_element.text
        texto_esperado_no_titulo = "Thanks for submitting the form"
              
        # A asserção agora verifica o texto do título do modal
        confirmacao_ok = texto_esperado_no_titulo.lower() in modal_title_text.lower()
      
        return confirmacao_ok

    def fechar_popup_confirmacao(self):
        """
        Fecha o modal de confirmação de envio.
        """
        close_button_locator = (By.ID, "closeLargeModal")
        close_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(close_button_locator))
        close_button.click()
        WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))