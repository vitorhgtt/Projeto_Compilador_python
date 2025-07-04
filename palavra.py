from tokens import Token


class Palavra:
    def __init__(self, token: Token, linha: int, lexema=None):
        self.token = token
        self.lexema = lexema
        self.linha = linha

    def __repr__(self):
        return f'Token(LEXEMA: {self.lexema}, LINHA: {self.linha}, COD: {self.token})' if self.lexema else f'Token(LINHA: {self.linha}, COD: {self.token})'
