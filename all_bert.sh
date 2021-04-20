rm -rf result
mkdir result
for i in 1 2 4 8 
do
    ./profile.sh python bert.py 0 $i
    cp output.csv bert_result/bert_3080_$i.csv
    ./profile.sh python bert.py 1 $i
    cp output.csv bert_result/bert_1080_$i.csv
done
