from parsing import *
from sympy import init_printing
from sympy import symbols
from sympy.matrices import Matrix
from Simulations import *
import pprint

init_printing(use_unicode=True)

netlist = read_file("net1")
Circuit_Matrix = parser(netlist)
# pprint.pprint(Circuit_Matrix)

#####################solve numerically direct####################
print("##########################solve numerically direct#########################")
Y, V, J = solve_dc_numerically(Circuit_Matrix)
print(Y[1:, 1:])
print(J[1:])
Result = Solve_Linear_Matrix(Y, J)
for i in range(len(V)):
    print(f"{V[i]} = {Result[i]}")
print("##########################solve symbolically###########################")
#######################solve symbolically########################
Y, V, J = solve_dc_Symbolically(Circuit_Matrix)
pprint.pprint(Y[1:, 1:])
pprint.pprint(J[1:,:])
Result =  Solve_Linear_Matrix_symbolically(Y, J)
for i in range(len(V)):
    print(f"{V[i]} = {Result[i]}")
print("##############################substitute###############################")
###########################substitute############################
Y, V, J = solve_dc_Symbolically(Circuit_Matrix)
Y = substitute(Y,Circuit_Matrix)
J = substitute(J,Circuit_Matrix)
pprint.pprint(Y[1:, 1:])
pprint.pprint(J[1:,:])
Result = substitute(Result,Circuit_Matrix)
for i in range(len(V)):
    pprint.pprint(f"{V[i]} = {Result[i]}")