  @web
Feature: Interação com Novas Janelas (Browser Windows)

  @web
  Scenario: Abrir nova janela e validar conteúdo
    Given que estou na página inicial do DemoQA
    When escolho a opção "Alerts, Frame & Windows" na página inicial
    And clico no submenu "Browser Windows"
    And clico no botão "New Window"
    Then uma nova janela deve ser aberta
    And a nova janela deve conter a mensagem "This is a sample page"
    And fecho a nova janela
    And volto para a janela original