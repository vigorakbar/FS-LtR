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
GRAPH_PATH = linePath[3][:-1]

def init_relevance():
  relArr = np.zeros(NODE_SIZE)
  print('initialize relevance score...')
  # NGULI MODE ON LOL
  relArr[0], relArr[1], relArr[2], relArr[3], relArr[4], relArr[5] , relArr[6], relArr[7], \
  relArr[8], relArr[9], relArr[10], relArr[11], relArr[12], relArr[13], relArr[14], relArr[15], \
  relArr[16], relArr[17], relArr[18], relArr[19], relArr[21], relArr[22], relArr[23], relArr[25], \
  relArr[26], relArr[27], relArr[28], relArr[29], relArr[30], relArr[31], relArr[32], relArr[33], \
  relArr[34], relArr[35], relArr[36], relArr[37], relArr[38], relArr[39], relArr[40], relArr[41], \
  relArr[43], relArr[44], relArr[45], relArr[46], relArr[47], relArr[48], relArr[49], relArr[50], \
  relArr[51], relArr[52], relArr[53], relArr[54], relArr[55], relArr[56], relArr[57], relArr[58], \
  relArr[59], relArr[60], relArr[61], relArr[62], relArr[63], relArr[64], relArr[65], relArr[66], \
  relArr[67], relArr[68], relArr[69], relArr[70], relArr[71], relArr[72], relArr[73], relArr[74], \
  relArr[75], relArr[76], relArr[77], relArr[78], relArr[79], relArr[80], relArr[81], relArr[82], \
  relArr[83], relArr[84], relArr[85], relArr[86], relArr[87], relArr[88], relArr[89], relArr[90], \
  relArr[91], relArr[92], relArr[93], relArr[94], relArr[100], relArr[101], relArr[102], relArr[103], \
  relArr[104], relArr[105], relArr[106], relArr[107], relArr[108], relArr[109], relArr[110], relArr[111], \
  relArr[112], relArr[113], relArr[114], relArr[115], relArr[116], relArr[117], relArr[118], relArr[119], \
  relArr[120], relArr[121], relArr[122], relArr[123], relArr[124], relArr[125], relArr[126], relArr[127], \
  relArr[128], relArr[129], relArr[130], relArr[131], relArr[132], relArr[133], relArr[134], relArr[135] = \
  26, 17, 39, 21, 29, 27, 21, 15, 1, 42, 141, 51, 40, 177, 116, 225, 171, 156, 236, 253, 41, 40, 30, 32, \
  23, 20, 5, 34, 11, 12, 19, 3, 17, 10, 42, 44, 28, 14, 3, 14, 29, 7, 2, 32, 65, 64, 9, 96, 34, 41, 77, 139, \
  54, 8, 14, 34, 93, 68, 13, 32, 60, 89, 63, 39, 37, 82, 83, 43, 65, 24, 70, 18, 62, 34, 54, 167, 64, 14, 23, \
  19, 70, 8, 17, 42, 36, 59, 20, 1, 4, 7, 32, 3, 70, 62, 53, 35, 91, 82, 72, 202, 180, 138, 48, 198, 83, 102, \
  78, 36, 243, 117, 104, 65, 40, 134, 102, 79, 77, 149, 188, 48, 249, 212, 398, 204, 179, 192, 95, 29
  
  normRelArr = (relArr - np.min(relArr))/np.ptp(relArr)
  for i in range(NODE_SIZE):
    G.nodes[i]['relevance'] = normRelArr[i]

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
