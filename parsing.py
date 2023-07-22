from typing import List, Dict

def read_file(file_path: str) -> List[str]:
    """
    This Function take file_path as an argument and return a li
    """
    # read the file
    raw_netlist = open(file_path, "r")

    # read all lines in a list
    raw_netlist_lines = raw_netlist.readlines()

    # remove the /n at the end of each line
    for i in range(0, len(raw_netlist_lines)):
        raw_netlist_lines[i] = raw_netlist_lines[i][:-1]

    return raw_netlist_lines[1:]

def element_Parsing(line: str) -> Dict:
    """
    This Function parse element_line to its parameters into dictionary as follows
    dict={"instance_name", "from", "to", "value", "unit"}
    """
    line_split = line.split()
    dict = {
        "instance_name": line_split[0],
        "from": int(line_split[1]),
        "to": int(line_split[2]),
        "value": int(line_split[3][:-1]) if not line_split[3][-1].isdigit() else int(line_split[3]),
        "unit": line_split[3][-1] if not line_split[3][-1].isdigit() else "nothing"
    }
    return dict

def analysis_Parsing(line: str) -> Dict:

    line_split = line.split()
    if line_split[0][1:] != "End":
        dict = {
            "analysis_type": line_split[0][1:],
        }
        return dict

def Get_Number_of_Nets(circuit_dict: dict):  # -> [int ,Dict] :
    """
    This Function determine and return the number of nets in the circuit
    """
    number_of_nets = 0
    for i, val in enumerate(circuit_dict):
        if circuit_dict[val] != [] and val != "num_nets" and val != "analysis":
            for j, v in enumerate(circuit_dict[val]):
                number_of_nets = max(number_of_nets, v['from'], v['to'])

    return number_of_nets

def parser(raw_netlist: list) -> Dict:
    circuit_dict = {
        "analysis": [],
        "num_nets": int,
        "resistor_list": [],
        "vsource_list": [],
        "isource_list": [],
    }

    for i, line in enumerate(raw_netlist):
        if line.startswith('R'):
            circuit_dict["resistor_list"].append(element_Parsing(line))
        elif line.startswith('V'):
            circuit_dict["vsource_list"].append(element_Parsing(line))
        elif line.startswith('I'):
            circuit_dict["isource_list"].append(element_Parsing(line))
        elif line.startswith('.'):
            x = analysis_Parsing(line)
            if x != None:
                circuit_dict["analysis"].append(x)

        circuit_dict["num_nets"] = Get_Number_of_Nets(circuit_dict)
    return circuit_dict
