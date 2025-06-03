# Projeto de Automação de Testes com Behave e Selenium (DemoQA)

Este projeto contém testes automatizados para o site DemoQA, abrangendo tanto testes de interface de usuário (Web) quanto testes de API. Ele utiliza Python com Behave para BDD (Behavior-Driven Development) e Selenium WebDriver para interação com a interface web.

## Funcionalidades Testadas

1.  **Cadastro de Usuário via Interface Web:**
    * Navegação para o formulário de "Practice Form".
    * Preenchimento de todos os campos do formulário, incluindo nome, sobrenome, email, gênero, número de celular, data de nascimento, hobbies, upload de imagem, endereço, estado e cidade.
    * Envio do formulário.
    * Verificação da mensagem de confirmação e fechamento do pop-up.
2.  **Fluxo Completo de API para Gerenciamento de Usuário e Livros:**
    * Geração de credenciais válidas.
    * Criação de um novo usuário.
    * Geração de token de autenticação para o usuário criado.
    * Verificação da autorização do usuário.
    * Listagem de todos os livros disponíveis na BookStore.
    * Seleção aleatória de dois livros.
    * Adição desses dois livros à coleção do usuário.
    * Verificação dos detalhes do usuário para confirmar a adição dos livros.

## Tecnologias Utilizadas

* **Python**: Linguagem de programação principal.
* **Behave**: Framework para Behavior-Driven Development (BDD).
* **Selenium WebDriver**: Para automação da interface do usuário web.
* **Requests**: Para interações com APIs HTTP.
* **webdriver-manager**: Para gerenciamento automático dos drivers do navegador (ex: ChromeDriver).

## Estrutura do Projeto
QA_Teste_Accenture/
├── features/                 # Arquivos Gherkin (.feature) e definições de steps
│   ├── steps/                # Implementações dos steps em Python
│   │   ├── cadastro_steps.py # Steps para o formulário de cadastro web
│   │   └── fluxo_completo_steps.py # Steps para o fluxo de API
│   ├── environment.py        # Hooks do Behave (before_scenario, after_step, etc.)
│   ├── cadastro_usuario.feature  # Cenários de teste para o cadastro web
│   └── fluxo_completo_api.feature # Cenários de teste para o fluxo de API
├── pages/                    # Page Objects para interação com as páginas web e APIs
│   ├── cadastro_page.py      # Page Object para a página de formulário de cadastro
│   ├── homepage.py           # Page Object para a página inicial do DemoQA
│   └── api_demoqa.py         # Page Object para as interações com a API DemoQA
├── utils/                    # Módulos utilitários
│   └── data_generator.py     # Gerador de dados (ex: credenciais)
├── data/                     # Pasta para arquivos de dados (ex: arquivo para upload)
│   └── Texto.txt             # Arquivo de exemplo para upload
├── screenshots_behave/       # Pasta onde os screenshots de cada step são salvos (criada em tempo de execução)
├── behave.ini                # Configurações do Behave (ex: captura de output)
├── requirements.txt          # Dependências do projeto Python
└── README.md                 # Este arquivo

## Pré-requisitos

* Python 3.x instalado.
* Google Chrome instalado (ou outro navegador, com ajustes no `environment.py`).
* Um ambiente virtual Python (recomendado).

## Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone <url_do_repositorio>
    cd QA_Teste_Accenture
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    Isso instalará Behave, Selenium, Requests, webdriver-manager e outras bibliotecas necessárias.

## Como Executar os Testes

### Executar todos os testes:
Navegue até a pasta raiz do projeto (`QA_Teste_Accenture`) e execute: 
```bash 
behave
```

## Executar um arquivo de feature específico: 
```bash 
behave features/nome_do_arquivo.feature
```
