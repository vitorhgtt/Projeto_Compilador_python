from palavra import Palavra
from tokens import Token, RESERVADAS, SIMBOLOS, PERMITIDOS
from sintatico import analisarSintaxe
from simbolos import TabelaDeSimbolos, Simbolo
from semantico import AnalisadorSemantico


class Lexico:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.simboloant = ""
        self.linha = 1
        self.caractere = 1
        self.char_atual = self.texto[self.pos] if self.pos < len(
            self.texto) else None

    def avancar(self):
        self.pos += 1
        self.caractere += 1
        if self.pos >= len(self.texto):
            self.char_atual = None
        else:
            self.char_atual = self.texto[self.pos]

        if (self.char_atual == '\n'):
            self.linha += 1
            self.caractere = 1

    def pular_espacos(self):
        while self.char_atual is not None and self.char_atual.isspace():
            self.avancar()

    def proximo_char(self):
        peek_pos = self.pos + 1
        return self.texto[peek_pos] if peek_pos < len(self.texto) else None
        # peek_pos = 0
        # peek_pos = self.pos + 1
        #  self.texto[peek_pos] if peek_pos < len(self.texto) else None

        # ret#urn self.texto[peek_pos] if peek_pos < len(self.texto) else None

    def tratar_string(self):
        resultado = ''
        self.avancar()  # Pula as aspas iniciais
        while self.char_atual is not None and self.char_atual != '"':
            if self.char_atual == '\\':
                self.avancar()  # Consome o '\'
                if self.char_atual is not None:
                    resultado += '\n'
                else:
                    raise Exception(
                        f"Erro léxico: Barra invertida isolada no final da string LINHA:{self.linha} POS:{self.caractere}")
            else:
                resultado += self.char_atual
            self.avancar()
        if self.char_atual != '"':
            raise Exception(
                f"Erro léxico: string não fechada LINHA:{self.linha} POS:{self.caractere}")
        palavra = Palavra(Token.STRING, self.linha, resultado)
        self.avancar()  # Pula as aspas finais
        return palavra

    def tratar_literal(self):
        resultado = ''
        self.avancar()  # Pula a aspa simples inicial
        while self.char_atual is not None and self.char_atual != "'":
            if self.char_atual == '\\':
                self.avancar()  # Consome o '\'
                if self.char_atual is not None:
                    resultado += '\n'
                else:
                    raise Exception(
                        "Erro léxico: Barra invertida isolada no final do literal LINHA:{self.linha} POS:{self.caractere}")
            else:
                resultado += self.char_atual
            self.avancar()
        if self.char_atual != "'":
            raise Exception(
                "Erro léxico: literal não fechado LINHA:{self.linha} POS:{self.caractere}")
        palavra = Palavra(Token.LITERAL, self.linha, resultado)
        self.avancar()  # Pula a aspa simples final
        return palavra

    def tratar_operadores(self):
        simbolo = self.char_atual
        # Verifica se há dois operadores consecutivos inválidos (ex: +-, --, */)
        if (self.simboloant is not None
            and (self.simboloant == "*" or self.simboloant == "/" or self.simboloant == "."
                 or self.simboloant == "+" or self.simboloant == "-")
            and (self.char_atual == "*" or self.char_atual == "/" or self.char_atual == "."
                 or self.char_atual == "+" or self.char_atual == "-")):
            raise Exception(
                f"Erro léxico: operadores inválidos em sequência LINHA:{self.linha} POS:{self.caractere}")

        # Se for um símbolo conhecido, retorna o token
        self.simboloant = simbolo
        palavra = Palavra(SIMBOLOS[simbolo], self.linha, simbolo)
        self.avancar()
        return palavra

        # raise Exception(f"Erro léxico: operador inválido ")

    def tratar_numero(self):
        resultado = ''
        tem_ponto = False
        original_pos = self.pos  # Guarda a posição original para rollback

    # Verifica se é um número negativo (sem espaços entre '-' e dígitos)

    # Coleta a parte inteira (pulando espaços já tratados)
        while self.char_atual is not None and self.char_atual.isdigit():
            resultado += self.char_atual
            self.avancar()

    # Verifica parte decimal
        if self.char_atual == '.':
            resultado += '.'
            tem_ponto = True
            self.avancar()
            if self.char_atual is None or not self.char_atual.isdigit():
                raise Exception(
                    "Erro léxico: Ponto decimal sem dígitos subsequentes LINHA:{self.linha} POS:{self.caractere}")
            while self.char_atual is not None and self.char_atual.isdigit():
                resultado += self.char_atual
                self.avancar()
        elif self.char_atual == ',' and self.proximo_char() is not None and self.proximo_char().isdigit():
            raise Exception(
                "Erro léxico: vírgula usada como separador decimal LINHA:{self.linha} POS:{self.caractere}")

    # Verifica se capturamos algum número válido
        if not resultado or resultado == '-':
            return None

    # Verifica os limites
        try:
            if tem_ponto:
                valor = float(resultado)
                token = Token.NREAL
            else:
                valor = int(resultado)
                token = Token.NINT
            if not (-2147483648 <= valor <= 2147483647):
                raise Exception(
                    "Erro léxico: número fora do intervalo permitido LINHA:{self.linha} POS:{self.caractere}")
        except ValueError:
            raise Exception(
                "Erro léxico: Formato de número inválido LINHA:{self.linha} POS:{self.caractere}")

        return Palavra(token, self.linha, resultado)

    def tratar_comentario_linha(self):
        while self.char_atual is not None and self.char_atual not in ('\n', '\r'):
            self.avancar()
        if self.char_atual is not None:
            self.avancar()

    def tratar_comentario_bloco(self):
        self.avancar()  # Consome o '?' inicial
        while self.char_atual is not None:
            if self.char_atual == '?':
                self.avancar()
                return
                # Se não for '?', continua procurando
            else:
                self.avancar()

        # Se chegou aqui, o comentário não foi fechado
        raise Exception(
            "Erro léxico: comentário de bloco não fechado LINHA:{self.linha} POS:{self.caractere}")

    def tratar_identificador(self):
        resultado = ''
        caracteres_permitidos = (
            'abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789_'
        )

        # Verifica se o primeiro caractere é válido (letra ou _)
        if not (self.char_atual.isalpha() or self.char_atual == '_'):
            raise Exception(
                f"Erro léxico: identificador deve começar com letra ou '_' (encontrado '{self.char_atual}') LINHA:{self.linha} POS:{self.caractere}")

        resultado += self.char_atual
        self.avancar()

        # Lê os próximos caracteres (apenas os permitidos)
        while self.char_atual is not None and (self.char_atual in caracteres_permitidos or self.char_atual in PERMITIDOS):
            if (self.char_atual in PERMITIDOS):
                token = RESERVADAS.get(resultado.lower(), Token.IDENT)
                return Palavra(token, self.linha, resultado)
            else:
                resultado += self.char_atual
                self.avancar()

        # Se parou em um caractere inválido (não é espaço, símbolo ou fim)
        if (self.char_atual is not None and
           not self.char_atual.isspace() and
           self.char_atual not in PERMITIDOS):
            raise Exception(
                f"Erro léxico: caractere inválido '{self.char_atual}' no identificador '{resultado}' LINHA:{self.linha} POS:{self.caractere}")

        # Verifica se é uma palavra reservada
        token = RESERVADAS.get(resultado.lower(), Token.IDENT)
        return Palavra(token, self.linha, resultado)

    def proxima_palavra(self):
        while self.char_atual is not None:
            if self.char_atual.isspace():
                self.pular_espacos()
                continue

            # verifiar simbolos de multiplos caracteres antes dos outros
            if self.char_atual == ':' and self.proximo_char() == '=':
                palavra = Palavra(Token.ATTRIB, self.linha, ':=')
                self.avancar()
                self.avancar()
                return palavra

            if self.char_atual == '>' and self.proximo_char() == '=':
                palavra = Palavra(Token.GTE, self.linha, '>=')
                self.avancar()
                self.avancar()
                return palavra

            if self.char_atual == '<':
                next_char = self.proximo_char()
                if next_char == '=':
                    palavra = Palavra(Token.LTE, self.linha, '<=')
                    self.avancar()
                    self.avancar()
                    return palavra
                elif next_char == '>':
                    palavra = Palavra(Token.DIFF, self.linha, '<>')
                    self.avancar()
                    self.avancar()
                    return palavra

            # 1. Verifica comentários ANTES de identificadores
            if self.char_atual == '!' and self.proximo_char() == '!':
                self.simboloant = ""
                self.avancar()  # Consome o primeiro '!'
                self.avancar()  # Consome o segundo '!'
                self.tratar_comentario_linha()
                continue

            if self.char_atual == '?':
                self.simboloant = ""
                self.avancar()  # Consome o '?'
                self.tratar_comentario_bloco()
                continue

            # 2. Strings e literais
            if self.char_atual == '"':
                self.simboloant = ""
                return self.tratar_string()
            if self.char_atual == "'":
                self.simboloant = ""
                return self.tratar_literal()

            # 3. Números (incluindo negativos)
            if self.char_atual.isdigit():
                num = self.tratar_numero()
                self.simboloant = ""
                if num is not None:
                    return num

            # 4. Identificadores (variáveis)
            if self.char_atual.isalpha() or self.char_atual == '_':
                self.simboloant = ""
                try:
                    return self.tratar_identificador()
                except Exception as e:
                    raise Exception(str(e))  # Repassa o erro léxico

            # 5. Símbolos (operadores, pontuação)
            if self.char_atual in SIMBOLOS:
                return self.tratar_operadores()
                # simbolo = self.char_atual
                # self.tratar_operadores()
                # self.avancar()
                # return Palavra(SIMBOLOS[simbolo], simbolo)
                # return self.tratar_operadores()
                # continue
                # simbolo = self.char_atual
                # self.avancar()
                # return Palavra(SIMBOLOS[simbolo], simbolo)

            # Se chegou aqui, é um caractere inválido
            raise Exception(
                f"Erro léxico: caractere inválido '{self.char_atual}' LINHA:{self.linha} POS:{self.caractere}")

        return Palavra(Token.EOF, self.linha, None)


palavras = []

with open('codigo_exemplo3.txt', 'r') as file:
    lexico = Lexico(file.read())
    palavraAtual = lexico.proxima_palavra()
    while palavraAtual.token != Token.EOF:
        print(palavraAtual.__repr__())
        palavras.append(palavraAtual)
        palavraAtual = lexico.proxima_palavra()
    print(palavraAtual)  # EOF


for p in palavras:
    print(f"Token: {p.token}")


# # SINTÁTICO
# resultado = analisarSintaxe(palavras)

# if resultado:
#     print("Código aceito pela análise sintática.")
# else:
#     print("Erro na análise sintática.")

resultado = analisarSintaxe(palavras)

if resultado:
    print("Código aceito pela análise sintática.")
    try:
        semantico = AnalisadorSemantico(palavras)
        if semantico.analisar():
            print("Código aceito pela análise semântica.")
    except Exception as e:
        print(str(e))
else:
    print("Erro na análise sintática.")
