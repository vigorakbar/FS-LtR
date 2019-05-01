import sys
import networkx as nx
import scipy.stats as ss
import numpy as np
import statistics
import time

pathFile = open('path.txt')
linePath = pathFile.readlines()
pathFile.close()

NODE_SIZE = 136
NDCG_PATH = linePath[0][:-1]
RANKS_PATH = linePath[1][:-1]
GRAPH_PATH = linePath[2][:-1]

def init_relevance():
  print('initialize relevance score...')
  for i in range(NODE_SIZE):
    relFile = open(NDCG_PATH+'NDCG'+str(i+1)+'.txt')
    lineList = relFile.readlines()
    relFile.close()
    G.nodes[i]['relevance'] = float(lineList[-3][22:-1])

def init_ranking():
  print('initialize ranking test result...')
  for i in range(NODE_SIZE):
    rankList = []
    rankSeq = []
    relFile = open(RANKS_PATH+'rank'+str(i+1)+'.txt')
    lineList = relFile.readlines()
    relFile.close()
    x = 0
    for j in range(len(lineList)):
      lineSeq = lineList[j][:-1].split('\t')
      if int(lineSeq[1]) == 0:
        if len(rankSeq) > 0:
          rankList.append(rankSeq)
        rankSeq = []
        rankSeq.append(float(lineSeq[2]))
        x += 1
      else:
        rankSeq.append(float(lineSeq[2]))
        x +=1
    if len(rankSeq) > 0:
          rankList.append(rankSeq)
    for j in range(len(rankList)):
      rankList[j] = ss.rankdata(rankList[j], method='ordinal')
    featureRankList.append(rankList)
    print(i)

def spearman(a, b, i):
  la = a.tolist()
  lb = b.tolist()
  if(len(la) == 1 or len(lb) == 1):
    return 1
  return np.cov(la,lb)[0][1]/(statistics.stdev(la)*statistics.stdev(lb))

def avg_spearman(a,b):
  return statistics.mean([spearman(a[i], b[i], i) for i in range(len(a))])

def init_similarity():
  print('initialize similarity score...')
  for i in range(NODE_SIZE):
    for j in range(i+1, NODE_SIZE):
      print("%.2f" % ((j/NODE_SIZE)*100) + "%" + " (%d" % (i+1) + "/" + "%d)" % NODE_SIZE)
      G[i][j]['similarity'] = float(avg_spearman(featureRankList[i], featureRankList[j]))

if __name__ == "__main__":
  print('initializing graph...')
  start = time.time()
  G = nx.complete_graph(NODE_SIZE)
  featureRankList = []
  init_relevance()
  init_ranking()
  init_similarity()
  nx.write_gexf(G, GRAPH_PATH)
  end = time.time()
  print('finished.')
  print('Graph initialization time:')
  print("%.2f" % (end - start) + " seconds")
