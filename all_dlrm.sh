for i in 1 2 4 8 
do
    CUDA_VISIBLE_DEVICES=0 ./profile.sh python dlrm/dlrm_s_pytorch.py --mini-batch-size=$i --test-mini-batch-size=$i --num-batches=1 --data-generation=random --arch-mlp-bot="128-64-32" --arch-mlp-top="256-64-1" --arch-sparse-feature-size="32" --arch-embedding-size="4000000-4000000-4000000-4000000-4000000-4000000-4000000-4000000" --num-indices-per-lookup="80" --num-indices-per-lookup-fixed="true" --arch-interaction-op="cat" --numpy-rand-seed=727 --inference-only --use-gpu --batch-size-test=1
    cp output.csv dlrm_result/dlrm_3080_$i.csv
    CUDA_VISIBLE_DEVICES=1 ./profile.sh python dlrm/dlrm_s_pytorch.py --mini-batch-size=$i --test-mini-batch-size=$i --num-batches=1 --data-generation=random --arch-mlp-bot="128-64-32" --arch-mlp-top="256-64-1" --arch-sparse-feature-size="32" --arch-embedding-size="4000000-4000000-4000000-4000000-4000000-4000000-4000000-4000000" --num-indices-per-lookup="80" --num-indices-per-lookup-fixed="true" --arch-interaction-op="cat" --numpy-rand-seed=727 --inference-only --use-gpu --batch-size-test=1
    cp output.csv dlrm_result/dlrm_1080_$i.csv
done
