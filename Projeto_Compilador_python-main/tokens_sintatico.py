from enum import Enum

class TokenSintatico(Enum):

    WHILE = 1
    VAR = 2
    TO = 3
    THEN = 4
    STRING = 5
    REAL = 6
    READ = 7
    PROGRAM = 8
    PROCEDURE = 9
    PRINT = 10
    NREAL = 11
    NINT = 12
    LITERAL = 13
    INTEGER = 14
    IF = 15
    IDENT = 16
    FOR = 17
    END = 18
    ELSE = 19
    DO = 20
    CONST = 21
    BEGIN = 22
    VSTRING = 23
    GTE = 24
    GT = 25
    EQ = 26
    DIFF = 27
    LTE = 28
    LT = 29
    MAIS = 30
    PVIRG = 31
    ATTRIB = 32
    DPONTO = 33
    FSLASH = 34
    PONTO = 35
    VIRG = 36
    ASTK = 37
    APARNT = 38
    FPARNT = 39
    ACHAVE = 40
    FCHAVE = 41
    MENOS = 42
    EOF = 43
    PROGRAMA = 45
    DECLARACOES = 46
    BLOCO = 47
    CONSTANTES = 48
    VARIAVEIS = 49
    PROCEDIMENTOS = 50
    COMANDOS = 51
    LISTAVARIAVEIS = 52
    TIPO = 53
    LDVAR = 54
    REPIDENT = 55
    PARAMETROS = 56
    REPARAMETROS = 57
    COMANDO = 58
    ITEMSAIDA = 59
    REPITEM = 60
    EXPRESSAO = 61
    TERMO = 62
    EXPR = 63
    FATOR = 64
    TER = 65
    EXPRELACIONAL = 66
    ELSEOPC = 67
    OPREL = 68
    CHAMADAPROC = 69
    LISTAPARAMETROS = 70
    PAR = 71
    REPPAR = 72

    @classmethod
    def getByCode(cls, code):
        for token in cls:
            if token.value == code:
                return token
        return None

    @property
    def lexeme(self):
        return self.name
