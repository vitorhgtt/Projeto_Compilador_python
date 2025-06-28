from tokens import Token

class Gramatica:
    def __init__(self):
        self.simbolo_inicial = 'PROGRAMA'
        
        self.producoes = {
            'PROGRAMA': [
               [Token.PROGRAM, Token.IDENT, Token.PVIRG, 'DECLARACOES', 'BLOCO', Token.PONTO]
           ],
            'DECLARACOES': [['CONSTANTES', 'VARIAVEIS', 'PROCEDIMENTOS']],
            'CONSTANTES': [
                ['const', 'ident', '=', 'nint', ';', 'CONSTANTES'],
                ['î']
            ],
            'VARIAVEIS': [['var', 'LISTAVARIAVEIS', ':', 'TIPO', ';', 'LDVAR']],
            'LISTAVARIAVEIS': [['ident', 'REPIDENT']],
            'REPIDENT': [
                ['î'],
                [',', 'ident', 'REPIDENT']
            ],
            'LDVAR': [
                ['LISTAVARIAVEIS', ':', 'TIPO', ';', 'LDVAR'],
                ['î']
            ],
            'TIPO': [
                ['integer'],
                ['real'],
                ['string']
            ],
            'PROCEDIMENTOS': [
                ['procedure', 'ident', 'PARAMETROS', ';', 'BLOCO', ';', 'PROCEDIMENTOS'],
                ['î']
            ],
            'PARAMETROS': [
                ['(', 'LISTAVARIAVEIS', ':', 'TIPO', 'REPPARAMETROS', ')'],
                ['î']
            ],
            'REPPARAMETROS': [
                [',', 'LISTAVARIAVEIS', ':', 'TIPO', 'REPPARAMETROS'],
                ['î']
            ],
            'BLOCO': [['begin', 'COMANDOS', 'end']],
            'COMANDOS': [
                ['COMANDO', ';', 'COMANDOS'],
                ['î']
            ],
            'COMANDO': [
                ['print', '{', 'ITEMSAIDA', 'REPITEM', '}'],
                ['if', 'EXPRELACIONAL', 'then', 'BLOCO', 'ELSEOPC'],
                ['ident', 'CHAMADAPROC'],
                ['for', 'ident', ':=', 'EXPRESSAO', 'to', 'EXPRESSAO', 'do', 'BLOCO'],
                ['while', 'EXPRELACIONAL', 'do', 'BLOCO'],
                ['read', '(', 'ident', ')']
            ],
            'ITEMSAIDA': [['EXPRESSAO']],
            'REPITEM': [
                ['î'],
                [',', 'ITEMSAIDA', 'REPITEM']
            ],
            'EXPRESSAO': [['TERMO', 'EXPR']],
            'EXPR': [
                ['+', 'TERMO', 'EXPR'],
                ['-', 'TERMO', 'EXPR'],
                ['î']
            ],
            'TERMO': [['FATOR', 'TER']],
            'TER': [
                ['*', 'FATOR', 'TER'],
                ['/', 'FATOR', 'TER'],
                ['î']
            ],
            'FATOR': [
                ['(', 'EXPRESSAO', ')'],
                ['ident'],
                ['nint'],
                ['nreal'],
                ['literal'],
                ['vstring']
            ],
            'EXPRELACIONAL': [['EXPRESSAO', 'OPREL', 'EXPRESSAO']],
            'OPREL': [
                ['='],
                ['<>'],
                ['<'],
                ['>'],
                ['<='],
                ['>=']
            ],
            'ELSEOPC': [
                ['else', 'BLOCO'],
                ['î']
            ],
            'CHAMADAPROC': [
                ['LISTAPARAMETROS'],
                [':=', 'EXPRESSAO']
            ],
            'LISTAPARAMETROS': [
                ['(', 'PAR', 'REPPAR', ')'],
                ['î']
            ],
            'PAR': [
                ['ident'],
                ['nint'],
                ['nreal'],
                ['vstring'],
                ['literal']
            ],
            'REPPAR': [
                [',', 'PAR', 'REPPAR'],
                ['î']
            ]
        }
    
    def obter_producao(self, nao_terminal, numero_producao):
        # Converte o número da produção para índice (subtrai 1 e remove .0)
        indice = int(numero_producao) - 1
        
        if nao_terminal in self.producoes and 0 <= indice < len(self.producoes[nao_terminal]):
            return self.producoes[nao_terminal][indice]
        
        raise ValueError(f"Produção {numero_producao} inválida para {nao_terminal}")    