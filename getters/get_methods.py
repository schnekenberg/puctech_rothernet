

def get_cpf(message : str) -> int:
    
    for letter in message:
        if isinstance(letter, int):

def is_interaction_over(message : str) -> bool:
    message = message.lower().strip()
    is_over = False

    if "voltarei com seu pedido em breve" in message:
        is_over = True
    
    return is_over


def has_interaction_started(message : str) -> bool:
    message = message.lower().strip()
    has_started = False

    if "Bem vindo ao restaurante" in message:
        has_started = True
        
    return has_started
        