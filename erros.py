class ErroSintatico(Exception):
    def __init__(self, mensagem, linha):
        super().__init__(f"Erro sintático na linha {linha}: {mensagem}")
        self.mensagem = mensagem
        self.linha = linha

class ErroGramatica(Exception):
    def __init__(self, mensagem):
        super().__init__(f"Erro na gramática: {mensagem}")
        self.mensagem = mensagem