from typing import Dict,List
import numpy as np
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

def res_stamp(Y : np.array , from_node : int  , to_node : int , res_value :float):
    from_node = from_node
    to_node = to_node

    Y[from_node][from_node] += 1 / res_value
    Y[to_node][to_node] += 1 / res_value
    Y[from_node][to_node] += -1 / res_value
    Y[to_node][from_node] += -1 / res_value
    return Y

def idc_stamp(J : np.array , from_node : int  , to_node : int , I_value :int):

    J[from_node] = -I_value
    J[to_node] = I_value
    return J

def vdc_stamp(Y : np.array, J : np.array ,from_node : int  , to_node : int , v_value :int , vdc_num : int):
        Y[from_node][vdc_num] = 1
        Y[to_node][vdc_num] = -1
        Y[vdc_num][to_node] = -1
        Y[vdc_num][from_node] = 1

        J[vdc_num] += v_value
        return Y, J

