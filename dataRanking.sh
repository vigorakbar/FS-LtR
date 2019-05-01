echo "Rank Test Data with Feature Models"
STARTTIME=$(date +%s)
for n in $(seq 1 136)
do
    echo "feature: "$n
    java -jar RankLib-2.1-patched.jar \
	-load "models/model"$n".txt" -rank MSLR-WEB10K/Fold1/test.txt -silent \
	-score "ranks/rank"$n".txt" \
	> "ranksInfo/rankInfo"$n".txt"
done
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to rank test data with all feature models" > dataRankingTime.txt
