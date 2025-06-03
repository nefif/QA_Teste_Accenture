from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.homepage import HomePage # Supondo que a navegação inicial use HomePage
from pages.progress_bar_page import ProgressBarPage
import time

# A step "Given que estou na página inicial do DemoQA" e
# "When escolho a opção "{card_name}" na página inicial"
# podem ser reutilizadas de outros arquivos de steps se já existirem e forem compatíveis.
# Se não, defina-as aqui ou em um arquivo de steps comum.

# Exemplo (se não existirem em outro lugar):
@given('que eu estou na página inicial do DemoQA')
def step_estou_pagina_inicial(context):
    if not hasattr(context, 'home_page') or context.home_page is None:
        context.home_page = HomePage(context.driver)
    context.home_page.abrir()

@when('escolho a opção "{card_name}" na página inicial do DemoQA')
def step_escolho_opcao_card(context, card_name):
    # Idealmente, HomePage teria um método para clicar em cards pelo nome.
    # Exemplo para "Widgets":
    if card_name == "Widgets":
        elemento = context.driver.find_element(By.XPATH, f"//h5[text()='{card_name}']/ancestor::div[@class='card mt-4 top-card']")
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        elemento.click()
    else:
        raise NotImplementedError(f'A lógica para clicar no card "{card_name}" não foi implementada.')

@when('clico no submenu "{submenu_name}" do DemoQA')
def step_clico_submenu(context, submenu_name):
    # XPath para "Progress Bar"
    if submenu_name == "Progress Bar":
        elemento = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{submenu_name}']"))
        )
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        elemento.click()
        context.progress_bar_page = ProgressBarPage(context.driver) # Inicializa a Page Object
    else:
        raise NotImplementedError(f'A lógica para clicar no submenu "{submenu_name}" não foi implementada.')


@when('clico no botão "Start" da barra de progresso')
def step_clico_start_progress_bar(context):
    context.progress_bar_page.click_start_stop_reset_button()

@when('paro a barra de progresso antes de "{valor_limite}"')
def step_paro_progress_bar_antes_de(context, valor_limite):
    parou_antes = context.progress_bar_page.stop_progress_before_value(valor_limite)
    # Você pode adicionar uma asserção aqui se for crítico que pare *sempre* antes,
    # mas o próximo step fará a validação do valor.
    # assert parou_antes, f"Não foi possível parar a barra de progresso antes de {valor_limite}"


@then('o valor da barra de progresso deve ser menor ou igual a "{valor_esperado_str}"')
def step_valida_valor_progress_bar_menor_igual(context, valor_esperado_str):
    valor_esperado = int(valor_esperado_str.replace('%',''))
    valor_atual = context.progress_bar_page.get_progress_bar_value()
    print(f"DEBUG: Validação - Valor atual: {valor_atual}%, Esperado <= {valor_esperado}%")
    assert valor_atual <= valor_esperado, \
        f"Valor da barra de progresso é {valor_atual}%, esperado menor ou igual a {valor_esperado}%."

@when('clico no botão "Start" da barra de progresso novamente')
def step_clico_start_novamente(context):
    # O botão pode estar como "Start" ou "Stop". Se estiver "Stop", já foi parado.
    # Se o objetivo é reiniciar um ciclo, e ele está parado, precisa ser "Start".
    # A lógica em click_start_stop_reset_button não diferencia, apenas clica.
    # Para ser mais explícito, podemos verificar o texto.
    button_text = context.progress_bar_page.get_button_text()
    if button_text.lower() == "start":
        context.progress_bar_page.click_start_stop_reset_button()
    elif button_text.lower() == "stop": # Se estiver em "Stop", significa que está rodando.
        print("DEBUG: Botão já está como 'Stop', progresso provavelmente em andamento.")
        # Se o teste anterior parou, e agora queremos 'Start' novamente,
        # o botão deveria estar como 'Start' ou 'Reset'.
        # Se o teste anterior parou o progresso, o botão deve ter voltado para 'Start'.
        # Se este step é chamado após um 'Stop', o botão estará 'Start'.
        pass # Assume que está pronto para o progresso continuar ou foi resetado

@when('espero a barra de progresso atingir "{valor_alvo_str}"')
def step_espero_progress_bar_atingir(context, valor_alvo_str):
    context.progress_bar_page.wait_for_progress_to_reach_value(valor_alvo_str)

@then('o botão da barra de progresso deve mudar para "{texto_esperado}"')
def step_valida_texto_botao_progress_bar(context, texto_esperado):
    # Pode levar um instante para o texto do botão mudar após atingir 100%
    WebDriverWait(context.driver, 5).until(
        lambda driver: context.progress_bar_page.get_button_text().lower() == texto_esperado.lower()
    )
    texto_botao_atual = context.progress_bar_page.get_button_text()
    print(f"DEBUG: Texto do botão: {texto_botao_atual}, Esperado: {texto_esperado}")
    assert texto_botao_atual.lower() == texto_esperado.lower(), \
        f"Texto do botão é '{texto_botao_atual}', esperado '{texto_esperado}'."

@then('clico no botão "Reset" da barra de progresso')
def step_clico_reset_progress_bar_then(context): # Nome da função diferente para evitar conflito se houver outra
    assert context.progress_bar_page.get_button_text().lower() == "reset", "Botão não está como Reset antes de clicar."
    context.progress_bar_page.click_start_stop_reset_button()
    time.sleep(0.5)


@then('o valor da barra de progresso deve ser "{valor_esperado_str}"')
def step_valida_valor_progress_bar_exato(context, valor_esperado_str):
    valor_esperado = int(valor_esperado_str.replace('%',''))
    # Após o reset, o valor pode demorar um instante para atualizar no DOM ou pode não ter o 'aria-valuenow' imediatamente
    # Tentaremos algumas vezes ou esperaremos um pouco
    valor_atual = -1 # Valor inicial improvável
    for _ in range(5): # Tenta por 0.5s
        valor_atual = context.progress_bar_page.get_progress_bar_value()
        if valor_atual == valor_esperado:
            break
        time.sleep(0.1)

    print(f"DEBUG: Validação - Valor atual: {valor_atual}%, Esperado: {valor_esperado}%")
    assert valor_atual == valor_esperado, \
        f"Valor da barra de progresso é {valor_atual}%, esperado {valor_esperado}%."