@web
Feature: Manipular os dados da tela Web Tables
  
  @web  
  Scenario: Adicionar novos valores a tabela
    Given que estou na página inicial
    And clico na opção Elements
    And clico na opção Web Tables
    When clico em Add
    And preencho os campos 
    And clico em Submit
    Then o valor será exibido na tela Web Pages

  @web  
  Scenario: Editar o novo registro criado na tabela 
    Given que estou na página inicial
    And clico na opção Elements
    And clico na opção Web Tables
    When crio um novo registro na tabela
    And clico em na opção de editar
    And altero os valores dos campos 
    And clico em Submit
    Then os novos valores serão exibidos na tela Web Pages

  @web  
  Scenario: Deletar o novo registro criado na tabela 
    Given que estou na página inicial
    And clico na opção Elements
    And clico na opção Web Tables
    When crio um novo registro na tabela
    And clico em na opção de excluir
    Then o registro é excluido 

  @web  
  Scenario: Criar e Deletar novos registros criado na tabela 
    Given que estou na página inicial
    And clico na opção Elements
    And clico na opção Web Tables
    When crio um novo registro na tabela
    And clico em na opção de excluir
    Then o registro é excluido 