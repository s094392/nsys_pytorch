rm -rf result
mkdir result
for i in 1 2 4 8 16
do
    ./profile.sh python resnet.py 0 $i
    cp output.csv result/ResNet_3080_$i.csv
    ./profile.sh python resnet.py 1 $i
    cp output.csv result/ResNet_1080_$i.csv
done
