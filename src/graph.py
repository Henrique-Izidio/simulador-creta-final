import heapq
from typing import Union

class Node:
    id: int
    isEntry: bool
    isExit: bool

    _routingTable: dict[int, dict[str, int]]
    _neighbors: list[dict[str, int]]

    def __init__(self, id: int, isEntry: bool, isExit: bool) -> None:
        self.id = id
        self.isEntry = isEntry
        self.isExit = isExit
        self._routingTable = {}
        self._neighbors = []
    
    def addNeighbor(self, neighboringNode: int, connectedByEdge: int, cost: int) -> None:
        newNeighbor: dict[str, int] = {
            "node" : neighboringNode,
            "edge" : connectedByEdge,
            "cost" : cost
        }
        self._neighbors.append(newNeighbor)
    
    def getNeighbors(self) -> list[dict[str, int]]:
        return self._neighbors

    def setRoutingTable(self, newRoutingTable: dict[int, dict[str, int]]) -> None:
        self._routingTable = newRoutingTable
    
    def getRoutingTable(self) -> dict[int, dict[str, int]]:
        return self._routingTable
    
    def getShortestPathTo(self, nodeId) -> dict[str, int]:
        return self._routingTable[nodeId]

class Edge:
    id: int
    cost: int
    nodeUId: int
    nodeVId: int

    def __init__(self, id: int, cost: int, uId: int, vId: int):
        self.id = id
        self.cost = cost
        self.nodeUId = uId
        self.nodeVId = vId

class Graph:

    _nodes: list[Node]
    _edges: list[Edge]

    def __init__(self, graphData) -> None:
        self._nodes = []
        self._edges = []       
        for nodeData in graphData["nodes"]:
            self._createNode(nodeData)
        
        for edgeData in graphData["edges"]:
            self._createEdge(edgeData)
        
        self._setRoutingTable()
    
    @classmethod
    def from_txt_format(cls, n, edges, entrada, saida):
        g = cls.__new__(cls)
        g._nodes = []
        g._edges = []
        
        for i in range(1, n + 1):
            is_entry = (i == entrada)
            is_exit = (i == saida)
            node = Node(i, is_entry, is_exit)
            g._nodes.append(node)
        
        edge_id = 1
        for u, v, w in edges:
            edge = Edge(edge_id, w, u, v)
            g._edges.append(edge)
            
            node_u = g.getNodeById(u)
            node_v = g.getNodeById(v)
            
            if node_u and node_v:
                node_u.addNeighbor(v, edge_id, w)
                node_v.addNeighbor(u, edge_id, w)
            
            edge_id += 1
        
        g._setRoutingTable()
        return g

    def _createNode(self, nodeData: dict[str, int]) -> None:
        newNode = Node(nodeData["id"], nodeData["isEntry"], nodeData["isExit"])
        self._nodes.append(newNode)

    def _createEdge(self, edgeData: dict[str, int]) -> None:
        newEdge = Edge(
            edgeData["id"],
            edgeData["cost"],
            edgeData["extremities"][0],
            edgeData["extremities"][1]
        )

        nodeU = self.getNodeById(newEdge.nodeUId)
        nodeU.addNeighbor(newEdge.nodeVId, newEdge.id, newEdge.cost)

        nodeV = self.getNodeById(newEdge.nodeVId)
        nodeV.addNeighbor(newEdge.nodeUId, newEdge.id, newEdge.cost)

        self._edges.append(newEdge)
    
    def getNodes(self) -> list[Node]:
        return self._nodes
    
    def getNodeById(self, nodeId) -> Node:
        for node in self._nodes:
            if (node.id == nodeId):
                return node
        return None

    def getEntry(self):
        for node in self._nodes:
            if(node.isEntry):
                return node.id

    def getExit(self):
        for node in self._nodes:
            if(node.isExit):
                return node.id
    
    def getEdges(self) -> list[Edge]:
        return self._edges
    
    def getEdgeById(self, edgeId) -> Edge:
        for edge in self._edges:
            if (edge.id == edgeId):
                return edge
        return None      

    def _dijkstra(self, startNodeId: int) -> dict[int, dict[str, int]]:
        
        distances: dict[int, Union[int, float]] = {node.id: float('inf') for node in self._nodes}
        distances[startNodeId] = 0
        
        routingTable: dict[int, dict[str, int]] = {}
        
        priority_queue = [(0, startNodeId)]

        nextHopTracker: dict[int, int] = {}
        
        while priority_queue:
            current_cost, u_id = heapq.heappop(priority_queue)
            
            if current_cost > distances[u_id]:
                continue
            
            u_node = self.getNodeById(u_id)
            
            for neighbor in u_node.getNeighbors():
                v_id = neighbor["node"]
                weight = neighbor["cost"]
                
                new_cost = current_cost + weight
                
                if new_cost < distances[v_id]:
                    distances[v_id] = new_cost
                    if u_id == startNodeId:
                        nextHopTracker[v_id] = v_id
                    elif u_id in nextHopTracker:
                        nextHopTracker[v_id] = nextHopTracker[u_id]
                    
                    heapq.heappush(priority_queue, (new_cost, v_id))
        
        for target_id, cost in distances.items():
            if cost != float('inf') and target_id != startNodeId:
                next_hop = nextHopTracker.get(target_id)
                if next_hop is not None:
                    routingTable[target_id] = {
                        'nextHop': next_hop,
                        'pathCost': int(cost)
                    }
        
        routingTable[startNodeId] = {
            'nextHop': startNodeId,
            'pathCost': 0
        }

        return routingTable

    def _setRoutingTable(self):
        for node in self._nodes:
            routingTable = self._dijkstra(node.id)
            node.setRoutingTable(routingTable)