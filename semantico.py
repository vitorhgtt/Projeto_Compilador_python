from palavra import Palavra
from tokens import Token as Token
from sintatico import analisarSintaxe
from simbolos import TabelaDeSimbolos, Simbolo

##erros que estão sendo tratados:
# atribuição de valores de tipos diferentes ao declarado de uma variável.

# modifcação de constantes.

class AnalisadorSemantico:
    def __init__(self, palavras):
        self.palavras = palavras
        self.pos = 0
        self.ts = TabelaDeSimbolos()
        self.nivel = 0  # escopo global

    def token_atual(self):
        if self.pos < len(self.palavras):
            return self.palavras[self.pos]
        return None

    def avancar(self):
        self.pos += 1

    def consumir(self, esperado):
        token = self.token_atual()
        if token.token != esperado:
            raise Exception(f"[Erro Semântico] Esperado {esperado}, mas encontrou {token.lexema} na linha {token.linha}")
        self.avancar()
        return token

    def analisar(self):
        while self.pos < len(self.palavras):
            token = self.token_atual()
            if token.token == Token.CONST:
                self.analisar_constantes()
            elif token.token == Token.VAR:
                self.analisar_variaveis()
            elif token.token == Token.IDENT:
                self.analisar_comando()
            else:
                self.avancar()  # pula outros tokens por enquanto
        self.ts.listar()
        return True

    def analisar_constantes(self):
        self.consumir(Token.CONST)
        while self.token_atual().token == Token.IDENT:
            nome = self.consumir(Token.IDENT).lexema
            self.consumir(Token.EQ)
            valor = self.token_atual()
            tipo = self.inferir_tipo_token(valor.token)
            self.ts.inserir(Simbolo(nome, 'constante', tipo, self.nivel))
            self.avancar()
            self.consumir(Token.PVIRG)

    def analisar_variaveis(self):
        self.consumir(Token.VAR)
        while self.token_atual().token == Token.IDENT:
            nomes = [self.consumir(Token.IDENT).lexema]
            while self.token_atual().token == Token.VIRG:
                self.avancar()
                nomes.append(self.consumir(Token.IDENT).lexema)
            self.consumir(Token.DPONTO)
            tipo = self.consumir_tipo()
            for nome in nomes:
                self.ts.inserir(Simbolo(nome, 'variável', tipo, self.nivel))
            self.consumir(Token.PVIRG)

    def consumir_tipo(self):
        token = self.token_atual()
        if token.token == Token.INTEGER:
            self.avancar()
            return 'integer'
        elif token.token == Token.REAL:
            self.avancar()
            return 'real'
        elif token.token == Token.STRING:
            self.avancar()
            return 'string'
        else:
            raise Exception(f"[Erro Semântico] Tipo inválido: {token.lexema} na linha {token.linha}")

    def analisar_comando(self):
        ident = self.consumir(Token.IDENT)
        if self.token_atual().token == Token.ATTRIB:
            self.consumir(Token.ATTRIB)
            valor = self.token_atual()
            tipo_valor = self.inferir_tipo_token(valor.token)
            simbolo = self.ts.buscar(ident.lexema)
            if not simbolo:
                raise Exception(f"[Erro Semântico] Variável '{ident.lexema}' não declarada.")
            if simbolo.tipo != tipo_valor:
                raise Exception(f"[Erro Semântico] Atribuição inválida na linha {ident.linha}: '{ident.lexema}' é {simbolo.tipo}, recebeu {tipo_valor}")
            self.avancar()
            if self.token_atual().token == Token.PVIRG:
                self.avancar()
            if simbolo.categoria == 'constante':
                raise Exception(f"[Erro Semântico] Modificação ilegal da constante '{ident.lexema}' na linha {ident.linha}.")


    def inferir_tipo_token(self, token_type):
        if token_type == Token.NINT:
            return "integer"
        elif token_type == Token.NREAL:
            return "real"
        elif token_type in (Token.LITERAL, Token.VSTRING, Token.STRING):
            return "string"
        elif token_type == Token.IDENT:
            simbolo = self.ts.buscar(self.token_atual().lexema)
            return simbolo.tipo if simbolo else "desconhecido"
        return "desconhecido"