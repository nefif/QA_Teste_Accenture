@web
Feature: Exibir mensagem ao abrir nova janela
  
  @web  
  Scenario: 
    Given que estou na página inicial
    And clico na opção Alerts, Frame & Windows
    And clico na opção Browser Windows
    When clico em New Window
    Then vizualizo uma nova janela
    And valido conteúdo da mensagem This is a sample page
    And fecho a nova janela