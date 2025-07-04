class Simbolo:
    def __init__(self, nome, categoria, tipo, nivel):
        self.nome = nome
        self.categoria = categoria
        self.tipo = tipo
        self.nivel = nivel

class TabelaDeSimbolos:
    def __init__(self):
        self.simbolos = []

    def inserir(self, simbolo):
        if self.buscar(simbolo.nome):
            raise Exception(f"Erro semântico: Identificador '{simbolo.nome}' já declarado.")
        self.simbolos.append(simbolo)

    def buscar(self, nome):
        for s in reversed(self.simbolos):
            if s.nome == nome:
                return s
        return None

    def remover_nivel(self, nivel):
        self.simbolos = [s for s in self.simbolos if s.nivel != nivel]

    def listar(self):
        print(f"\n{'Nome':<10} | {'Categoria':<10} | {'Tipo':<10} | {'Nível':<5}")
        print("-" * 40)
        for s in self.simbolos:
            print(f"{s.nome:<10} | {s.categoria:<10} | {s.tipo:<10} | {s.nivel:<5}")
