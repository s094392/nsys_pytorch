import ast
import json
import csv
import argparse

def parse_dict(filename):
    data = list()
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            data.append(ast.literal_eval(line))
    return data

def parse_json(filename):
    data = json.load(open(filename))
    M = dict()
    for i in data:
        M[i["CorrId"]] = i
    return M


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-j", "--json", help="nsys outputed json file")
    parser.add_argument("-d", "--dict", help="pyprof parsed dict file")
    parser.add_argument("-o", "--output", help="output csv filename")
    args = parser.parse_args()

    layer_info = parse_dict(args.dict)
    kernel_info = parse_json(args.json)

    op = layer_info[0]["op"] or ["_"]  
    now_duration = int(layer_info[0]["kDuration"])
    now_reg = kernel_info[layer_info[0]["cid"]]["Reg/Trd"]
    now_smem = kernel_info[layer_info[0]["cid"]]["StcSMem"]

    data = list()
    for i in range(1, len(layer_info)):
        current_kernel = kernel_info[layer_info[i]["cid"]]
        if layer_info[i]["op"] != op:    
            if op == "":
                op = ["_"]
            data.append({"Op": op[0], "duration": now_duration, "Reg/Trd": now_reg, "StcSMem": now_smem})
            now_duration = 0    
            now_reg = 0
            now_smem = 0
        now_duration += int(layer_info[i]["kDuration"])
        now_reg = max((now_reg, int(current_kernel["Reg/Trd"])))
        now_smem = max((now_reg, int(current_kernel["StcSMem"])))
        op = layer_info[i]["op"]
        
    data.append({"Op": op[0], "duration": now_duration, "Reg/Trd": now_reg, "StcSMem": now_smem})

    keys = data[0].keys()
    with open(args.output, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

if __name__ == "__main__":
    main()
