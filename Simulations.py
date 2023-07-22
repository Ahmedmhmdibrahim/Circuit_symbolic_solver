import Numerical_stamping
import Analytical_stamping
from sympy import init_printing
from sympy import symbols
from sympy.matrices import Matrix
import numpy as np
from typing import List

init_printing(use_unicode=True)

Convert_unit_to_value = {'G': 1e9,
                         'M': 1e6,
                         'K': 1e3,
                         'm': 1e-3,
                         'u': 1e-6,
                         'n': 1e-9,
                         'p': 1e-12,
                         "f": 1e-15,
                         'nothing': 1
                         }

def solve_dc_numerically(elements):
    n = elements["num_nets"] + len(elements["vsource_list"])
    Y = np.zeros([n+1, n+1])
    J = np.zeros([n+1, 1])
    V = []

    # Construct Unknown Vector 'V'
    for i in range(elements["num_nets"]):
        V.append(f"V{i+1}")

    for element in elements["resistor_list"]:
        from_node = element["from"]
        to_node = element["to"]
        value = element["value"] * Convert_unit_to_value[element["unit"]]
        Numerical_stamping.res_stamp(Y, from_node = from_node , to_node= to_node , res_value= value)

    for element in elements["isource_list"]:
        from_node = element["from"]
        to_node = element["to"]
        value = element["value"] * Convert_unit_to_value[element["unit"]]
        Numerical_stamping.idc_stamp(J, from_node = from_node , to_node= to_node , I_value= value)

    position =  elements["num_nets"]
    for i, element in enumerate(elements["vsource_list"]):
        from_node = element["from"]
        to_node = element["to"]
        vdc_num = position + i + 1
        v_value = element["value"] * Convert_unit_to_value[element["unit"]]
        V.append("I_" + element["instance_name"])
        Numerical_stamping.vdc_stamp(Y, J, from_node = from_node , to_node= to_node , v_value= v_value , vdc_num = vdc_num)

    return Y, V, J

def solve_dc_Symbolically(elements):
    n = elements["num_nets"] + len(elements["vsource_list"])
    Y_temp = np.zeros([n+1, n+1])
    J_temp = np.zeros([n+1, 1])
    Y = Matrix(Y_temp)
    J = Matrix(J_temp)
    V = []
    # Construct Unknown Vector 'V'
    for i in range(elements["num_nets"]):
        V.append(f"V{i+1}")

    for element in elements["resistor_list"]:
        from_node = element["from"]
        to_node = element["to"]
        value = symbols(element["instance_name"])
        Analytical_stamping.res_stamp(Y, from_node = from_node , to_node= to_node , res_value= value)

    for element in elements["isource_list"]:
        from_node = element["from"]
        to_node = element["to"]
        value = symbols(element["instance_name"])
        Analytical_stamping.idc_stamp(J, from_node = from_node , to_node= to_node , I_value= value)

    position =  elements["num_nets"]
    for i, element in enumerate(elements["vsource_list"]):
        from_node = element["from"]
        to_node = element["to"]
        vdc_num = position + i + 1
        value = symbols(element["instance_name"])
        V.append("I_" + element["instance_name"])
        Analytical_stamping.vdc_stamp(Y, J, from_node = from_node , to_node= to_node , v_value= value , vdc_num = vdc_num)

    return Y, V, J

def Solve_Linear_Matrix(Y: np.array, J: np.array) -> List:
    Y = Y[1:len(Y), 1:len(Y)]
    J = J[1:len(J)]
    return np.linalg.solve(Y, J)

def Solve_Linear_Matrix_symbolically(Y: Matrix, J: Matrix) -> List:
    Y = Y[1:, 1:]
    J = J[1:,:]
    return Y.solve(J)

def substitute_Y(Y: Matrix , elements):
    for element in elements["resistor_list"]:
        value = element["value"] * Convert_unit_to_value[element["unit"]]
        symbole = symbols(element["instance_name"])
        Y = Y.subs(symbole, value)
    return Y

def substitute(X: Matrix , elements):
    for element in elements["resistor_list"]:
        value = element["value"] * Convert_unit_to_value[element["unit"]]
        symbole = symbols(element["instance_name"])
        X = X.subs(symbole, value)

    for element in elements["isource_list"]:
        value = element["value"] * Convert_unit_to_value[element["unit"]]
        symbole = symbols(element["instance_name"])
        X = X.subs(symbole, value)

    for element in elements["vsource_list"]:
        value = element["value"] * Convert_unit_to_value[element["unit"]]
        symbole = symbols(element["instance_name"])
        X = X.subs(symbole, value)

    return X