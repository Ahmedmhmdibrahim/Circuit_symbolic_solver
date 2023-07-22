from sympy.matrices import Matrix

def res_stamp(Y : Matrix , from_node : int  , to_node : int , res_value :float):

    Y[from_node,from_node] += 1 / res_value
    Y[to_node,to_node] += 1 / res_value
    Y[from_node,to_node] += -1 / res_value
    Y[to_node,from_node] += -1 / res_value
    return Y

def idc_stamp(J : Matrix , from_node : int  , to_node : int , I_value :int):
    J[from_node] = -I_value
    J[to_node] = I_value
    return J

def vdc_stamp(Y : Matrix, J : Matrix ,from_node : int  , to_node : int , v_value :int , vdc_num : int):
        Y[from_node,vdc_num] = 1
        Y[to_node,vdc_num] = -1
        Y[vdc_num,to_node] = -1
        Y[vdc_num,from_node] = 1

        J[vdc_num] += v_value
        return Y, J

