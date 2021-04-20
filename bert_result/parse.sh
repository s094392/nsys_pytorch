for i in *.csv
do
    echo $i
    python parse.py $i > grouped_$i
done
