from graph import Graph
import random

class Prisioneiro:
    def __init__(self, pos_inicial):
        self.pos = pos_inicial
        self.trajetoria = [pos_inicial]
        self.vivo = True
        self.escapou = False
        
        self.visitados = {pos_inicial}
        self.arestas = set()
        self.volta = []
    
    def mover_para(self, novo):
        if self.vivo and not self.escapou:
            aresta = tuple(sorted([self.pos, novo]))
            self.arestas.add(aresta)

            self.volta.append(self.pos)

            self.pos = novo
            self.trajetoria.append(novo)
            self.visitados.add(novo)
    
    def ja_visitou(self, v):
        return v in self.visitados
    
    def ja_percorreu_aresta(self, u, v):
        aresta = tuple(sorted([u, v]))
        return aresta in self.arestas
    
    def escolher_proximo_movimento(self, g):
        node = g.getNodeById(self.pos)
        if node is None:
            return None

        vizinhos = node.getNeighbors()
        random.shuffle(vizinhos)

        for viz in vizinhos:
            v = viz["node"]
            if not self.ja_visitou(v) and not self.ja_percorreu_aresta(self.pos, v):
                return v
        while self.volta:
            ultimo = self.volta.pop()
            if not self.ja_percorreu_aresta(self.pos, ultimo):
                return ultimo
        return None

class Minotauro:
    def __init__(self, posicao_inicial, percepcao, graph: Graph):
        self.startPosition = posicao_inicial
        self.actualPosition = posicao_inicial
        self.path = [posicao_inicial]
        self.labyrinthMap = graph
        self.perception = percepcao
        
        self.inChase = False
        self.findMoment = None
        self.chasePath = []
        self.reachMoment = None
    
    def move(self, prisonerPosition):
        if(len(self.chasePath) == 0): self.chasePath.append(self.actualPosition)
        
        nextMove = None
        pathToPrisoner = self.labyrinthMap.getNodeById(self.actualPosition).getShortestPathTo(prisonerPosition)

        dist = pathToPrisoner.get("pathCost", float('inf'))

        if(self.perception >= dist):
            self.inChase = True
            nextMove = pathToPrisoner["nextHop"]
            self.path.append(nextMove)
            self.chasePath.append(nextMove)

            pathToPrisoner = self.labyrinthMap.getNodeById(nextMove).getShortestPathTo(prisonerPosition)
            nextMove = pathToPrisoner["nextHop"]
            if(self.path[-1] != nextMove):
                self.path.append(nextMove)
                self.chasePath.append(nextMove)
        else:
            self.inChase = False
            nextMove = self.randomChoiceMove()
            self.path.append(nextMove)
        
        self.actualPosition = nextMove
    
    def chaseMove(self):
        pass
    
    def randomChoiceMove(self):
        node = self.labyrinthMap.getNodeById(self.actualPosition)
        if node is None:
            return self.actualPosition

        neighbors = node.getNeighbors()
        if not neighbors:
            return self.actualPosition

        neighbor_ids = [n["node"] for n in neighbors]

        last = self.path[-1] if len(self.path) > 0 else None
        candidates = [nid for nid in neighbor_ids if nid != last]
        if not candidates:
            chosen = neighbor_ids[0]
        else:
            chosen = random.choice(candidates)
        return chosen

    def setFindMoment(self, findMoment):
        self.findMoment = findMoment