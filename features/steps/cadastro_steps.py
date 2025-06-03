from behave import given, when, then
from pages.homepage import HomePage
from pages.cadastro_page import CadastroPage

@given("que estou na página inicial")
def step_abre_pagina_inicial(context):
    context.home = HomePage(context.driver)
    context.home.abrir()

@given("clico na opção Forms")
def step_clica_menu_forms(context):
    context.home.clicar_menu_forms()

@given("clico na opção Practice Form")
def step_clica_practice_form(context):
    context.home.clicar_practice_form()

@when("preencho todos os campos do formulário")
def step_preenche_campos_principais(context): 
    if not hasattr(context, 'form'):
        context.form = CadastroPage(context.driver)
    context.form.preencher_campos_principais()

@when("faço upload de arquivo")
def step_faz_upload_arquivo(context):
    if not hasattr(context, 'form'):
        context.form = CadastroPage(context.driver)
    context.form.fazer_upload_arquivo()

@when("envio o formulário")
def step_envia_formulario(context):
    context.form.enviar_formulario()

@when("devo ver a confirmação de envio com os dados preenchidos")
def step_confirma_envio(context):
    assert context.form.verificar_confirmacao(), "Confirmação de envio não foi exibida"

@then("fecho o pop-up") 
def step_fecha_popup(context): 
    if not hasattr(context, 'form'):
        context.form = CadastroPage(context.driver)
    context.form.fechar_popup_confirmacao() 
