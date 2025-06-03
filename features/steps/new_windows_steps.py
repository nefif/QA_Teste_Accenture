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
    # Método genérico para clicar em um card na HomePage
    # Pode ser necessário adicionar um método mais específico em HomePage ou usar XPaths genéricos
    # Exemplo:
    # context.home_page.clicar_card_pelo_nome(card_name)
    # Por agora, vou usar o XPATH específico para "Alerts, Frame & Windows"
    if card_name == "Alerts, Frame & Windows":
        elemento = context.driver.find_element(By.XPATH, "//h5[text()='Alerts, Frame & Windows']/ancestor::div[@class='card mt-4 top-card']")
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        elemento.click()
    else:
        raise NotImplementedError(f'A lógica para clicar no card "{card_name}" não foi implementada.')

@when('clico no submenu "{submenu_name}"')
def step_clico_submenu(context, submenu_name):
    # Método genérico para clicar em um item de submenu
    # XPath para "Browser Windows"
    if submenu_name == "Browser Windows":
        elemento = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Browser Windows']"))
        )
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        elemento.click()
        context.new_windows_page = NewWindowsPage(context.driver) # Inicializa a Page Object específica
    else:
        raise NotImplementedError(f'A lógica para clicar no submenu "{submenu_name}" não foi implementada.')

@when('clico no botão "New Window"')
def step_clico_new_window(context):
    context.new_windows_page.clicar_new_window_button()
    # Armazena o handle da janela original ANTES de qualquer switch, se ainda não foi feito
    # No entanto, é melhor pegar o handle original no método da Page Object que faz o switch.
    # Aqui apenas guardamos os handles *depois* do clique, para referência.
    context.original_window_handle = context.driver.current_window_handle
    # Espera um pouco para a nova janela realmente abrir, se necessário
    WebDriverWait(context.driver, 10).until(EC.number_of_windows_to_be(2))
    context.all_window_handles_after_click = context.driver.window_handles


@then('uma nova janela deve ser aberta')
def step_valida_nova_janela_aberta(context):
    # A validação de que uma nova janela foi aberta é implícita se o próximo step (verificar msg) funcionar
    # Mas podemos verificar explicitamente o número de janelas
    assert len(context.all_window_handles_after_click) > 1, "Nenhuma nova janela foi aberta."
    # Encontra o handle da nova janela
    context.new_window_handle = None
    for handle in context.all_window_handles_after_click:
        if handle != context.original_window_handle:
            context.new_window_handle = handle
            break
    assert context.new_window_handle is not None, "Handle da nova janela não encontrado."


@then('a nova janela deve conter a mensagem "{mensagem_esperada}"')
def step_valida_mensagem_nova_janela(context, mensagem_esperada):
    # O método da Page Object já faz o switch e a verificação
    # Ele precisa do handle da nova janela, que já identificamos no step anterior.
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
    # Garante que estamos na nova janela antes de fechar
    if context.driver.current_window_handle == context.new_window_handle:
        context.driver.close()
    else:
        # Se por algum motivo o foco não estiver na nova janela, mude para ela e feche
        context.driver.switch_to.window(context.new_window_handle)
        context.driver.close()


@then('volto para a janela original')
def step_volto_janela_original(context):
    context.driver.switch_to.window(context.original_window_handle)
    assert context.driver.current_window_handle == context.original_window_handle, \
        "Não foi possível retornar para a janela original."