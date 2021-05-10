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

def get_thread_num(kernel):
    return kernel["GrdX"] * kernel["GrdY"] * kernel["GrdZ"] * kernel["BlkX"] * kernel["BlkY"] * kernel["BlkZ"]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-j", "--json", help="nsys outputed json file")
    parser.add_argument("-d", "--dict", help="pyprof parsed dict file")
    parser.add_argument("-o", "--output", help="output csv filename")
    args = parser.parse_args()

    layer_info = parse_dict(args.dict)
    kernel_info = parse_json(args.json)

    op = layer_info[0]["op"] or ["_"]  
    first_kernel = kernel_info[layer_info[0]["cid"]]
    now_duration = int(layer_info[0]["kDuration"])
    now_reg = first_kernel["Reg/Trd"]
    now_smem = first_kernel["StcSMem"] + first_kernel["StcSMem"]
    now_thread = get_thread_num(first_kernel)

    data = list()
    for i in range(1, len(layer_info)):
        current_kernel = kernel_info[layer_info[i]["cid"]]
        if layer_info[i]["op"] != op:    
            if op == "":
                op = ["_"]
            data.append({"Op": op[0], "duration": now_duration, "Reg/Trd": now_reg, "Mem": now_smem, "Thread": now_thread})
            now_duration = 0    
            now_reg = 0
            now_smem = 0
            now_thread
        now_duration += int(layer_info[i]["kDuration"])
        now_reg = max((now_reg, int(current_kernel["Reg/Trd"])))
        now_smem = max((now_reg, int(current_kernel["StcSMem"]) + int(current_kernel["DymSMem"])))
        now_thread = max(now_thread, get_thread_num(current_kernel))
        op = layer_info[i]["op"]
        
    data.append({"Op": op[0], "duration": now_duration, "Reg/Trd": now_reg, "Mem": now_smem, "Thread": now_thread})

    keys = data[0].keys()
    with open(args.output, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

if __name__ == "__main__":
    main()
