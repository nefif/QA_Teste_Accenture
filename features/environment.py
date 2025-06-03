import os
from datetime import datetime
from selenium import webdriver

SCREENSHOTS_DIR = os.path.join(os.getcwd(), "screenshots_behave")

def before_all(context):
    """
    Executado uma vez antes de todos os features e cenários.
    Cria o diretório de screenshots se não existir.
    """
    if not os.path.exists(SCREENSHOTS_DIR):
        os.makedirs(SCREENSHOTS_DIR)
    print(f"Diretório de screenshots configurado em: {SCREENSHOTS_DIR}")

def before_scenario(context, scenario):
    """
    Executado antes de cada cenário.
    Limpa dados de testes de API e inicializa o WebDriver para cenários @web.
    """
    # Limpa dados usados nos testes de API
    context.username = None
    context.password = None
    context.response_create = None
    context.user_id = None
    context.username_returned = None
    context.response_token = None
    context.token = None
    context.auth_header = None
    context.response_auth = None
    context.response_list = None
    context.livros_list = None
    context.isbn1 = None
    context.isbn2 = None
    context.title1 = None
    context.title2 = None
    context.response_add = None
    context.added_response = None
    context.response_details = None
    context.details_response = None

    # Verifica se o cenário está marcado com @web para iniciar o driver
    if "web" in scenario.tags:
        try:
            context.driver = webdriver.Chrome()
            context.driver.maximize_window()
        except Exception as e:
            print(f"FALHA na inicialização do WebDriver: {e}")
            raise 

def after_step(context, step):
    """
    Executado após cada step.
    Tira um screenshot se o WebDriver estiver ativo.
    """
    if hasattr(context, 'driver') and context.driver:
        try:
            max_len = 40 
            
            feature_name_raw = getattr(context.feature, 'name', 'feature_desconhecida')
            scenario_name_raw = getattr(context.scenario, 'name', 'cenario_desconhecido')
            step_name_raw = step.name
            
            # Função auxiliar para sanitizar e truncar nomes
            def sanitize_name(name, length=max_len):
                name_sanitized = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name)
                name_sanitized = name_sanitized.replace(' ', '_').lower()
                return name_sanitized[:length]

            feature_name = sanitize_name(feature_name_raw)
            scenario_name = sanitize_name(scenario_name_raw)
            step_name = sanitize_name(step_name_raw, length=60) 

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            
            current_feature_dir = os.path.join(SCREENSHOTS_DIR, feature_name)
            if not os.path.exists(current_feature_dir):
                os.makedirs(current_feature_dir)
            
            current_scenario_dir = os.path.join(current_feature_dir, scenario_name)
            if not os.path.exists(current_scenario_dir):
                os.makedirs(current_scenario_dir)

            filename = f"step_{step_name}_{timestamp}.png"
            filepath = os.path.join(current_scenario_dir, filename)
            
            context.driver.save_screenshot(filepath)
            if hasattr(step, 'text'): 
                step.text = f"{step.text}\nScreenshot: {filepath}"

            print(f"Screenshot salvo: {filepath} (Status do Step: {step.status})")

        except Exception as e:
            print(f"Falha ao tirar screenshot para o step '{step.name}': {e}")

def after_scenario(context, scenario):
    """
    Executado após cada cenário.
    Fecha o navegador se ele foi iniciado.
    """
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()