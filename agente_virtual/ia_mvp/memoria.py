class MemoriaConversa:
    def __init__(self):
        self.historico = []

    def adicionar(self, usuario: str, agente: str):
        self.historico.append({"usuario": usuario, "agente": agente})

    def obter_historico(self):
        texto = ""
        for i, turno in enumerate(self.historico, 1):
            texto += f"\n[{i}] Usuário: {turno['usuario']}\n[{i}] Agente: {turno['agente']}"
        return texto