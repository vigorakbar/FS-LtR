echo "evaluate NGAS subsets"
STARTTIME=$(date +%s)
n=5
for i in $(seq 1 15)
do
    echo "subset ngas "$n
    java -jar RankLib-2.1-patched.jar \
        -train MSLR-WEB10K/Fold1/train.txt -test MSLR-WEB10K/Fold1/test.txt -ranker 0 -feature "FeatureSelection/results/ngas/sub"$n".txt" -silent \
        -metric2t NDCG@10 -save "models/ngas/ngas_model"$n".txt"\
        > "NDCGs/ngas/ngas"$n".txt"
    ((n+=5))
done
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to evaluate all NGAS subset"
