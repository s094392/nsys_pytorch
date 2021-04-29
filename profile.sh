nsys profile -f true -o net --export sqlite $@
nsys stats -r gputrace net.qdrep -f json -o net
python -m pyprof.parse net.sqlite > net.dict
python parse.py -j net_gputrace.json -d net.dict -o output.csv
rm -f net.dict net.qdrep net_gputrace.json net.sqlite
