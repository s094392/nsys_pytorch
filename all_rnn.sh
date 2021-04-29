for i in 1 2 4 8 
do
    ./profile.sh python rnn.py 0 $i
    cp output.csv rnn_result/rnn_3080_$i.csv
    ./profile.sh python rnn.py 1 $i
    cp output.csv rnn_result/rnn_1080_$i.csv
done
