import csv
import sys

def main():
    filename = sys.argv[1]
    with open(filename) as f:
        a = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]

    now = a[0]["Op"]
    now_sum = int(a[0]["Sil(ns)"])

    for i in range(1, len(a)):
        if a[i]["Op"] != now:
            if now == "":
                now = "_"
            print(now, ", ", now_sum)
            now_sum = 0
        now_sum += int(a[i]["Sil(ns)"])
        now = a[i]["Op"]
    print(now, ", ", now_sum)





if __name__ == "__main__":
    main()
