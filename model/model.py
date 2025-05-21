import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.retailers = DAO.getRetailers()
        self._idMap = {}
        for retailer in self.retailers:
            self._idMap[retailer.Retailer_code] = retailer

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

    def getMaxWieght(self,N):
        self.sol_ottima = -1
        self.path_ottimo = []
        for node in self._graph.nodes():
            path = [node]
            self.recursive(node,path,N)

    def recursive(self,node,path,N):
        if len(path) == N:
            if path[0] == path[-1]:
                return path
            return 0

        else:
            for nd in self._graph.neighbors(node):
                if nd not in path:
                    path.append(nd)
                    self.recursive(nd,path,N)





