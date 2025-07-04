from tokens_sintatico import TokenSintatico as enumToken
from tabela_parsing import matriz as TabelaParsing
from producoes import Producoes
from firstfollow import matriz as FirstFollow
from palavra import Palavra  # Importa sua classe Palavra

def getFirstFollow(tokens):
    s = ''
    for i in range(len(tokens)):
        s += enumToken.getByCode(tokens[i]).lexeme
        if i == len(tokens) - 2:
            s += " ou "
        elif i != len(tokens) - 1:
            s += " "
    return s

def analisarSintaxe(tokens):
    i = 0
    pilha = [43, 45]  # suponho que 43 = EOF, 45 = símbolo inicial

    tokens.append(Palavra(enumToken.EOF, 0, "$"))  # Adiciona EOF ao final da lista de tokens

    terminou = False
    while not terminou:
        print("\nPilha atual:", pilha)
        topo = pilha.pop()

        if i >= len(tokens):
            print("Erro: tokens esgotados, esperado EOF e encontrado:", enumToken.getByCode(topo).name)
            return False

        token_atual = tokens[i].token
        lexema_atual = tokens[i].lexema
        linha_atual = tokens[i].linha

        if topo < 43 or topo > 100:  # terminal
            print(f"Topo é terminal: {enumToken.getByCode(topo).name}, token atual: {enumToken.getByCode(token_atual).name} ('{lexema_atual}')")
            if topo == token_atual:
                print(f"Token '{lexema_atual}' aceito, avançando para próximo token.")
                i += 1
            else:
                print(f"Erro de sintaxe na linha {linha_atual}: esperado {enumToken.getByCode(topo).name} mas encontrado '{lexema_atual}'")
                print("Estado da pilha:", pilha)
                print("Tokens restantes:", [t.lexema for t in tokens[i:]])
                return False

        elif topo != 43:  # não-terminal
            print(f"Topo é não-terminal: {topo} ({enumToken.getByCode(topo).name if enumToken.getByCode(topo) else 'desconhecido'})")
            print(f"Token atual: {enumToken.getByCode(token_atual).name} ('{lexema_atual}') na linha {linha_atual}")

            producao = TabelaParsing[topo][token_atual]
            if producao != 0:
                print(f"Produção selecionada: {producao}")
                conteudo = Producoes.getByCode(producao).cpd
                if conteudo:
                    print("Empilhando símbolos (em ordem inversa):", conteudo[::-1])
                    for simbolo in conteudo[::-1]:
                        pilha.append(simbolo)
                else:
                    print("Produção é epsilon (vazia).")
            else:
                print(f"Erro de sintaxe na linha {linha_atual}: token '{lexema_atual}' inesperado para não-terminal {topo}")
                print(f"Esperado um dos: {getFirstFollow(FirstFollow[topo])}")
                print("Estado da pilha:", pilha)
                print("Tokens restantes:", [t.lexema for t in tokens[i:]])
                return False

        else:  # topo == 43 (EOF)
            # print(f"Topo é EOF, token atual: {enumToken.getByCode(token_atual).name}")
            if token_atual.value == 43:
                print("Análise sintática concluída com sucesso!")
                terminou = True
            else:
                print(f"Erro de sintaxe na linha {linha_atual}: esperado EOF mas encontrado '{lexema_atual}'")
                return False

    return True


