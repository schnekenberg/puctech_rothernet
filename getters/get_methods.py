
# def get_cpf(message : str) -> int: 
    

def is_interaction_over(message : str) -> bool:
    message = message.lower().strip()
    is_over = False

    if "voltarei com seu pedido em breve" in message:
        is_over = True
    
    return is_over


def has_interaction_started(message : str) -> bool:
    message = message.lower().strip()
    has_started = False

    if "bem-vindo ao restaurante" or "bem vindo ao restaurante" in message:
        has_started = True

    return has_started

def get_order_id(message: str) -> int | None:
    message = message.lower().strip()
    words = message.split()
    
    for i, word in enumerate(words):
        if word == "id" and i + 1 < len(words):
            next_word = words[i + 1]
            if next_word.isdigit() and len(next_word) == 2:
                return int(next_word)
    return None



        