@web
Feature: Cadastro de usuário no formulário da DemoQA
  
  @web  
  Scenario: Preencher o formulário de cadastro com dados válidos
    Given que estou na página inicial
    And clico na opção Forms
    And clico na opção Practice Form
    When preencho todos os campos do formulário
    And faço upload de arquivo
    And envio o formulário
    And devo ver a confirmação de envio com os dados preenchidos
    Then fecho o pop-up
