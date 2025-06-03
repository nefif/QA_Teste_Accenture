# utils/data_generator.py

import random
import string

def generate_credentials() -> tuple[str, str]:
    """
    Gera um par (username, password) que atende à política:
      - username: "qa_user_" + 6 caracteres alfanuméricos aleatórios
      - password: 12 caracteres, contendo ao menos 1 maiúscula, 1 minúscula, 1 dígito e 1 especial
    """
    # Username
    random_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    username = f"qa_user_{random_part}"

    # Senha
    specials = "!@#$%^&*"
    maius = random.choice(string.ascii_uppercase)
    minus = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special_char = random.choice(specials)
    restantes = "".join(random.choices(string.ascii_letters + string.digits + specials, k=8))

    senha_lista = list(maius + minus + digit + special_char + restantes)
    random.shuffle(senha_lista)
    password = "".join(senha_lista)

    return username, password
