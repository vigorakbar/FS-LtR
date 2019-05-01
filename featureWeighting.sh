echo "Weighting Feature"
STARTTIME=$(date +%s)
for n in $(seq 1 136)
do
    echo "feature: "$n
    java -jar RankLib-2.1-patched.jar \
	-train MSLR-WEB10K/Fold1/train.txt -test MSLR-WEB10K/Fold1/test.txt -ranker 0 -feature "featureDesc/feature"$n".txt" -silent \
	-metric2t NDCG@10 -save "models/model"$n".txt" \
	> "NDCGs/NDCG"$n".txt"
done
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to calculate all feature weight" > featureWeightingTime.txt
