import copy
from datetime import datetime
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.retailers = DAO.getRetailers()
        self._idMap = {}
        for retailer in self.retailers:
            self._idMap[retailer.Retailer_code] = retailer
        self._N = None

    def fillDD(self):
        countries = set()
        for ret in self.retailers:
            countries.add(ret.Country)
        return sorted(list(countries))

    def buildGraph(self,year,country):
        for ret in self.retailers:
            if ret.Country == country:
                self._graph.add_node(ret)
        allEdges = DAO.getAllEdges(year,country)
        for ed in allEdges:
            self._graph.add_edge(self._idMap[ed[0]],self._idMap[ed[1]],weight=ed[2])

    def findVolumes(self):
        volumi = {}
        for node in self._graph.nodes():
            somma = 0
            for arch in self._graph.edges(node,data=True):
                somma += arch[2]["weight"]
            volumi[node] = somma

        sorted_dict = dict(sorted(volumi.items(), key=lambda item: item[1], reverse=True))
        return sorted_dict

    def getMaxWeight(self,N):
        self._N = N
        self.sol_ottima = -1
        self.path_ottimo = []
        for node in self._graph.nodes():
            self.recursive([node],[],0)
        return

    def recursive(self,nodes,path,sum):
        if len(path) == self._N:   # ES: N=5, devo trovare 5 archi e 6 nodi in path (nodo in = nodo fin) ==> len(path) == 4
            if path[0][0] == path[-1][1]: # c'è un solo arco che connette due nodi
                if sum > self.sol_ottima:
                    self.sol_ottima = sum
                    self.path_ottimo = copy.deepcopy(path)
            return

        for edge in self._graph.edges(nodes[-1], data=True):
                if edge[1] not in nodes:
                    sum += edge[2]["weight"]
                    nodes.append(edge[1])
                    path.append(edge)
                    self.recursive(nodes,path,sum)
                    path.pop()
                    sum -= edge[2]["weight"]
                    nodes.pop()