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
            path = []
            sum = 0
            self.recursive(node,path,sum)

    def recursive(self,node,path,sum):
        if len(path) == self._N:   # ES: N=4, ho 4 archi quando in path ci sono 5 nodi ==> len(path) == 4
            for ar in self._graph.edges(node, data=True):
                if path[0] == ar[1]:
                    sum += ar[2]["weight"]
                    path.append(ar[1])
                    if sum > self.sol_ottima:
                        self.sol_ottima = sum
                        self.path_ottimo = path
                        print(f"la soluzione ottima ha peso {self.sol_ottima}")
                return

        else:
            for ar in self._graph.edges(node, data=True):
                if ar[1] not in path:
                    sum += ar[2]["weight"]
                    path.append(ar[1])
                    self.recursive(ar[1],path,sum)
                    path.pop()