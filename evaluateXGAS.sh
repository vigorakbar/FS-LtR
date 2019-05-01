echo "evaluate XGAS subsets"
STARTTIME=$(date +%s)
n=5
for i in $(seq 1 15)
do
    echo "subset xgas "$n
    java -jar RankLib-2.1-patched.jar \
        -train MSLR-WEB10K/Fold1/train.txt -test MSLR-WEB10K/Fold1/test.txt -ranker 0 -feature "FeatureSelection/results/xgas/sub"$n".txt" -silent \
        -metric2t NDCG@10 -save "models/xgas/xgas_model"$n".txt"\
        > "NDCGs/xgas/xgas"$n".txt"
    ((n+=5))
done
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to evaluate all XGAS subset"
