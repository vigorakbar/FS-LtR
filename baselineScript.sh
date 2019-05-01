echo "training all feature for baseline"
STARTTIME=$(date +%s)
java -jar RankLib-2.1-patched.jar \
-train MSLR-WEB10K/Fold1/train.txt -test MSLR-WEB10K/Fold1/test.txt -ranker 0 -silent \
-metric2t NDCG@10 -save models/modelBaseline.txt\
> NDCGs/NDCGBaseline.txt
ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to train all feature"
