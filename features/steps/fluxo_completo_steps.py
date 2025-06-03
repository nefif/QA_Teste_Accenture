# features/steps/fluxo_completo_steps.py

import random
from behave import given, when, then
from pages.api_demoqa import DemoQAAPI
from utils.data_generator import generate_credentials

@given('gero credenciais válidas')
def step_gera_credenciais(context):
    """
    Gera username e password aleatórios e exibe no console.
    """
    context.username, context.password = generate_credentials()
    print(f"\n[Passo] Credenciais geradas:")
    print(f"    → Username: {context.username}")
    print(f"    → Password: {context.password}")

@when('crio um usuário no endpoint "{path}"')
def step_cria_usuario(context, path):
    """
    Chama DemoQAAPI.criar_usuario() e exibe userID/username.
    """
    context.response_create = DemoQAAPI.criar_usuario(context.username, context.password)
    try:
        body = context.response_create.json()
    except ValueError:
        body = context.response_create.text

    if context.response_create.status_code == 201:
        context.user_id = body.get("userID")
        context.username_returned = body.get("username")
        print(f"[Passo] Usuário criado com sucesso:")
        print(f"    → userID: {context.user_id}")
        print(f"    → username retornado: {context.username_returned}")
    else:
        print(f"[Passo] Falha ao criar usuário. Status: {context.response_create.status_code}")
        print(f"    → Body: {body}")

@then('o status HTTP deve ser {expected_code:d}')
def step_valida_status(context, expected_code):
    """
    Valida status code da última response relevante (create, token, auth ou details).
    """
    if hasattr(context, "response_create"):
        response = context.response_create
    elif hasattr(context, "response_token"):
        response = context.response_token
    elif hasattr(context, "response_auth"):
        response = context.response_auth
    elif hasattr(context, "response_details"):
        response = context.response_details
    else:
        response = None

    assert response is not None, "Nenhuma response encontrada para validar status."
    actual = response.status_code
    assert actual == expected_code, (
        f"Esperado status {expected_code}, mas recebeu {actual}. Body: {response.text}"
    )

@then('armazeno o "userID" e o "username" gerado')
def step_armazenar_userid_username(context):
    """
    Garante que user_id e username_returned existem.
    """
    assert hasattr(context, "user_id"), "userID não armazenado."
    assert hasattr(context, "username_returned"), "username retornado não armazenado."

@when('gero um token usando "{path}"')
def step_gera_token(context, path):
    """
    Chama DemoQAAPI.gerar_token() e exibe o token.
    """
    context.response_token = DemoQAAPI.gerar_token(context.username, context.password)
    try:
        body = context.response_token.json()
    except ValueError:
        body = context.response_token.text

    if context.response_token.status_code == 200:
        context.token = body.get("token")
        print(f"[Passo] Token gerado com sucesso:")
        print(f"    → Token: {context.token}")
    else:
        print(f"[Passo] Falha ao gerar token. Status: {context.response_token.status_code}")
        print(f"    → Body: {body}")

@then('armazeno o "token" retornado')
def step_armazenar_token(context):
    """
    Garante que o token exista e prepara header de Authorization.
    """
    assert hasattr(context, "token") and context.token, "Token não armazenado."
    context.auth_header = {"Authorization": f"Bearer {context.token}"}

@when('verifico autorização no endpoint "{path}"')
def step_verifica_autorizacao(context, path):
    """
    Chama DemoQAAPI.verificar_autorizacao() e exibe status/body.
    """
    context.response_auth = DemoQAAPI.verificar_autorizacao(context.token)
    print(f"[Passo] Verificando autorização:")
    print(f"    → Status: {context.response_auth.status_code}")
    body = context.response_auth.text.strip()
    if body:
        snippet = body if len(body) < 100 else body[:100] + "..."
        print(f"    → Body: {snippet}")

@when('listo todos os livros disponíveis via "{path}"')
def step_lista_livros(context, path):
    """
    Chama DemoQAAPI.listar_livros() e exibe todos os títulos e ISBNs.
    """
    context.response_list = DemoQAAPI.listar_livros()
    assert context.response_list.status_code == 200, (
        f"Falha ao listar livros: {context.response_list.status_code}, {context.response_list.text}"
    )
    body = context.response_list.json()
    context.livros_list = body.get("books", [])
    print(f"[Passo] Listando livros disponíveis:")
    print(f"    → Total de livros: {len(context.livros_list)}")
    for idx, livro in enumerate(context.livros_list, start=1):
        titulo = livro.get("title", "<sem título>")
        isbn = livro.get("isbn", "<sem isbn>")
        print(f"       {idx}. '{titulo}' (ISBN={isbn})")

@then('devo ver pelo menos 2 livros retornados')
def step_valida_qtd_livros(context):
    """
    Verifica se há pelo menos 2 livros em context.livros_list.
    """
    assert hasattr(context, "livros_list"), "Lista de livros ausente."
    assert len(context.livros_list) >= 2, f"Apenas {len(context.livros_list)} livro(s) retornado(s)."

@then('armazeno a lista completa de livros')
def step_armazenar_lista_completa(context):
    """
    Garante que context.livros_list existe.
    """
    assert hasattr(context, "livros_list"), "Lista de livros não foi armazenada."

@when('seleciono dois livros aleatórios')
def step_seleciona_dois_livros(context):
    """
    Escolhe dois livros aleatórios de context.livros_list e exibe quais.
    """
    if len(context.livros_list) < 2:
        assert False, "Não há livros suficientes para seleção."
    escolhidos = random.sample(context.livros_list, 2)
    context.isbn1 = escolhidos[0].get("isbn")
    context.isbn2 = escolhidos[1].get("isbn")
    context.title1 = escolhidos[0].get("title")
    context.title2 = escolhidos[1].get("title")

    print(f"[Passo] Seleção aleatória de 2 livros:")
    print(f"    → Livro 1: '{context.title1}' (ISBN={context.isbn1})")
    print(f"    → Livro 2: '{context.title2}' (ISBN={context.isbn2})")

@then('armazeno os dois ISBNs escolhidos')
def step_armazenar_isbns(context):
    """
    Garante que context.isbn1 e context.isbn2 existem.
    """
    assert hasattr(context, "isbn1") and hasattr(context, "isbn2"), "ISBNs não foram definidos."

@when('adiciono esses dois livros ao usuário via "{path}"')
def step_adiciona_livros(context, path):
    """
    Chama DemoQAAPI.adicionar_livros() e exibe o resultado.
    """
    context.response_add = DemoQAAPI.adicionar_livros(
        context.user_id,
        context.token,
        [context.isbn1, context.isbn2]
    )
    status = context.response_add.status_code
    try:
        body = context.response_add.json()
    except ValueError:
        body = context.response_add.text

    print(f"[Passo] Adicionando os dois livros ao usuário:")
    print(f"    → Status: {status}")
    print(f"    → Body: {body if isinstance(body, str) else body}")

    assert status in (200, 201), f"Falha ao adicionar livros (status {status})."
    context.added_response = context.response_add.json()

@then('o status HTTP deve ser 200 ou 201 no response de adição')
def step_valida_status_adicao(context):
    """
    Verifica se context.response_add.status_code é 200 ou 201.
    """
    assert hasattr(context, "response_add"), "Nenhuma response_add encontrada para validação."
    actual = context.response_add.status_code
    assert actual in (200, 201), f"Esperado 200 ou 201, mas foi {actual}. Body: {context.response_add.text}"

@then('a resposta de adição deve conter exatamente os dois ISBNs selecionados')
def step_valida_adicao(context):
    """
    Verifica se response_add.json()['books'] contém exatamente os dois ISBNs.
    """
    books = context.added_response.get("books", [])
    assert isinstance(books, list) and len(books) == 2, f"Resposta inválida: {books}"
    isbns_retorno = {item.get("isbn") for item in books}
    esperado = {context.isbn1, context.isbn2}
    assert isbns_retorno == esperado, f"Esperado {esperado}, mas veio {isbns_retorno}"

@when('obtenho detalhes do usuário via "{path}"')
def step_obtem_detalhes_usuario(context, path):
    """
    Chama DemoQAAPI.detalhes_usuario() e exibe a lista de livros no perfil.
    """
    context.response_details = DemoQAAPI.detalhes_usuario(context.user_id, context.token)
    assert context.response_details.status_code == 200, (
        f"Falha ao obter detalhes do usuário: {context.response_details.status_code}, "
        f"{context.response_details.text}"
    )
    context.details_response = context.response_details.json()

    books = context.details_response.get("books", [])
    print(f"[Passo] Detalhes do usuário (books no perfil):")
    print(f"    → Quantidade de livros no perfil: {len(books)}")
    for idx, b in enumerate(books, start=1):
        isbn = b.get("isbn")
        title = b.get("title")
        print(f"       {idx}. '{title}' (ISBN={isbn})")

@then('o status HTTP deve ser 200 no response de detalhes')
def step_valida_status_detalhes(context):
    """
    Verifica se context.response_details.status_code é 200.
    """
    assert hasattr(context, "response_details"), "Nenhuma response_details encontrada para validação."
    actual = context.response_details.status_code
    assert actual == 200, f"Esperado 200, mas foi {actual}. Body: {context.response_details.text}"

@then('no campo "books" devem aparecer os ISBNs previamente adicionados')
def step_valida_books_no_perfil(context):
    """
    Verifica se context.details_response['books'] contém os ISBNs escolhidos.
    """
    books = context.details_response.get("books", [])
    isbns_perfil = {item.get("isbn") for item in books}
    esperado = {context.isbn1, context.isbn2}
    assert esperado.issubset(isbns_perfil), (
        f"ISBNs esperados {esperado} não encontrados. Perfil retornado: {isbns_perfil}"
    )
