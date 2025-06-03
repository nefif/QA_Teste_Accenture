# features/steps/new_windows_steps.py
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.homepage import HomePage # Supondo que a navegação inicial use HomePage
from pages.new_windows_page import NewWindowsPage

@given('que estou na página inicial do DemoQA')
def step_estou_pagina_inicial(context):
    context.home_page = HomePage(context.driver)
    context.home_page.abrir()

@when('escolho a opção "{card_name}" na página inicial')
def step_escolho_opcao_card(context, card_name):

    if card_name == "Alerts, Frame & Windows":
        elemento = context.driver.find_element(By.XPATH, "//h5[text()='Alerts, Frame & Windows']/ancestor::div[@class='card mt-4 top-card']")
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        elemento.click()
    else:
        raise NotImplementedError(f'A lógica para clicar no card "{card_name}" não foi implementada.')

@when('clico no submenu "{submenu_name}"')
def step_clico_submenu(context, submenu_name):

    if submenu_name == "Browser Windows":
        elemento = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Browser Windows']"))
        )
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        elemento.click()
        context.new_windows_page = NewWindowsPage(context.driver) 
    else:
        raise NotImplementedError(f'A lógica para clicar no submenu "{submenu_name}" não foi implementada.')

@when('clico no botão "New Window"')
def step_clico_new_window(context):
    context.new_windows_page.clicar_new_window_button()

    context.original_window_handle = context.driver.current_window_handle
    WebDriverWait(context.driver, 10).until(EC.number_of_windows_to_be(2))
    context.all_window_handles_after_click = context.driver.window_handles


@then('uma nova janela deve ser aberta')
def step_valida_nova_janela_aberta(context):

    assert len(context.all_window_handles_after_click) > 1, "Nenhuma nova janela foi aberta."
    context.new_window_handle = None
    for handle in context.all_window_handles_after_click:
        if handle != context.original_window_handle:
            context.new_window_handle = handle
            break
    assert context.new_window_handle is not None, "Handle da nova janela não encontrado."


@then('a nova janela deve conter a mensagem "{mensagem_esperada}"')
def step_valida_mensagem_nova_janela(context, mensagem_esperada):

    context.driver.switch_to.window(context.new_window_handle)
    try:
        mensagem_elemento = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.ID, context.new_windows_page.sample_heading_id))
        )
        mensagem_encontrada = mensagem_elemento.text
        print(f"DEBUG: Texto encontrado na nova janela (step): '{mensagem_encontrada}'")
        assert mensagem_esperada in mensagem_encontrada, \
            f"Mensagem esperada '{mensagem_esperada}' não encontrada. Encontrado: '{mensagem_encontrada}'"
    except Exception as e:
        print(f"DEBUG: Erro ao verificar mensagem na nova janela (step): {e}")
        assert False, f"Erro ao tentar validar mensagem na nova janela: {e}"


@then('fecho a nova janela')
def step_fecho_nova_janela(context):

    if context.driver.current_window_handle == context.new_window_handle:
        context.driver.close()
    else:

        context.driver.switch_to.window(context.new_window_handle)
        context.driver.close()


@then('volto para a janela original')
def step_volto_janela_original(context):
    context.driver.switch_to.window(context.original_window_handle)
    assert context.driver.current_window_handle == context.original_window_handle, \
        "Não foi possível retornar para a janela original."