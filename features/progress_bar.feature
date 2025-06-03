@web
Feature: Interação com a Barra de Progresso

  @web
  Scenario: Controlar e validar a barra de progresso
    Given que eu estou na página inicial do DemoQA
    When escolho a opção "Widgets" na página inicial do DemoQA
    And clico no submenu "Progress Bar" do DemoQA
    And clico no botão "Start" da barra de progresso
    And paro a barra de progresso antes de "25%"
    Then o valor da barra de progresso deve ser menor ou igual a "25%"
    When clico no botão "Start" da barra de progresso novamente
    And espero a barra de progresso atingir "100%"
    Then o botão da barra de progresso deve mudar para "Reset"
    Then clico no botão "Reset" da barra de progresso  # <--- Usando "Then" explicitamente
    Then o valor da barra de progresso deve ser "0%"