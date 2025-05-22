from model.model import Model

mymodel = Model()

mymodel.buildGraph(2016,"Germany")
mymodel.getMaxWeight(5)
print(mymodel.sol_ottima)
print(mymodel.path_ottimo)
