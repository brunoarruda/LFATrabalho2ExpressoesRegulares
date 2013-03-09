class NFA:
    def __init__(self, processaSimbolo = None):
        self.estados = []
        self.alfabeto = set([])
        self.transicao = {}
        self.estadoInicial = None
        self.estadosFinais = []
        if processaSimbolo:
            self.processaSimbolo = processaSimbolo
        else:
            self.processaSimbolo = lambda x: x
    
    def adiciona_estado(self, nome, transicao, st_inic=0, st_final=0):
        self.estados.append(nome)
        self.transicao[nome] = transicao

        simbolos = set(transicao.keys())
        self.alfabeto.union(simbolos)

        if st_inic:
            self.estadoInicial = nome
        if st_final:
            self.estadosFinais.append(nome)

    def executa(self, sentenca):
        if not self.estadoInicial:
                raise("Initialization Error", "deve existir um estado inicial")
        if not self.estadosFinais:
                raise("Initialization Error", "deve existir pelo menos um estado final")
        estadosAtuais = []
        estadosAtuais.append(self.estadoInicial)
        for simbolo in sentenca.split():
                simbolo = self.processaSimbolo(simbolo)
                aux = []
                for estadoAtual in estadosAtuais:
                    for cadaTransicao in self.transicao[estadoAtual][simbolo]:
                        aux.append(cadaTransicao)
                estadosAtuais = aux
        self.responde(estadosAtuais, sentenca)
        
    def responde(self, estadosAtuais, sentenca):
        auxResposta = ""        
        for estadoAtual in estadosAtuais: 
            if estadoAtual in self.estadosFinais:
                auxResposta += estadoAtual
        if auxResposta:
            print("A sentenca '" + sentenca + "' foi reconhecida pelo automato com estado final " + auxResposta + ".")
        else:
            print("A sentenca '" + sentenca + "' nao foi reconhecida pelo automato.")

