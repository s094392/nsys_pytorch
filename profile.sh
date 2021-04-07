nsys profile -f true -o net --export sqlite $@
python -m pyprof.parse net.sqlite > net.dict
python -m pyprof.prof --csv net.dict > output.csv
rm net.dict
