# features/fluxo_completo.feature

Feature: Fluxo completo de API DemoQA
  Testar todas as etapas da API DemoQA de forma sequencial e validada.

  Scenario: Executar fluxo de ponta a ponta
    Given gero credenciais válidas
    When crio um usuário no endpoint "/Account/v1/User"
    Then o status HTTP deve ser 201
    And armazeno o "userID" e o "username" gerado

    When gero um token usando "/Account/v1/GenerateToken"
    Then o status HTTP deve ser 201
    And armazeno o "token" retornado

    When verifico autorização no endpoint "/Account/v1/Authorized"
    Then o status HTTP deve ser 201

    When listo todos os livros disponíveis via "/BookStore/v1/Books"
    Then devo ver pelo menos 2 livros retornados
    And armazeno a lista completa de livros

    When seleciono dois livros aleatórios
    Then armazeno os dois ISBNs escolhidos

    When adiciono esses dois livros ao usuário via "/BookStore/v1/Books"
    Then o status HTTP deve ser 200 ou 201 no response de adição
    And a resposta de adição deve conter exatamente os dois ISBNs selecionados

    When obtenho detalhes do usuário via "/Account/v1/User/{user_id}"
    Then o status HTTP deve ser 200 no response de detalhes
    And no campo "books" devem aparecer os ISBNs previamente adicionados
