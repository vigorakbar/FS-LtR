import sys
import networkx as nx
import math

pathFile = open('path.txt')
linePath = pathFile.readlines()
pathFile.close()

GRAPH_PATH = linePath[2][:-1]
MAX_FEATURE_SUBSET = 50
TRADE_OFF = 0.5

def mmr():
  for i in range(MAX_FEATURE_SUBSET):
    mmr = {}
    nodes = nx.get_node_attributes(G, 'relevance')
    if (i != 0):
      for key1, value in nodes.items():
        diff_score = 0
        for key2 in feature_subset:
          if key1 < key2:
            sim = edges[key1, key2]
          else:
            sim = edges[key2, key1]
          diff_score = diff_score + (1 - sim)
        diff_score = (diff_score * TRADE_OFF) / len(feature_subset)
        mmr[key1] = (1 - TRADE_OFF) * value + diff_score
      max_rel = max(mmr.keys(), key=(lambda key: mmr[key]))
    else:
      max_rel = max(nodes.keys(), key=(lambda key: nodes[key]))
    feature_subset.append(max_rel)
    edges = nx.get_edge_attributes(G, 'similarity')
    G.remove_node(max_rel)

def msd():
  for i in range(len(G)):
    for j in range(i+1, len(G)):
      G[i][j]['msd'] = (1 - TRADE_OFF) * (G.nodes[i]['relevance'] + G.nodes[j]['relevance']) + 2 * TRADE_OFF * (1 - G[i][j]['similarity'])
  while len(feature_subset) < MAX_FEATURE_SUBSET:
    msds = nx.get_edge_attributes(G, 'msd')
    max_msd = max(msds.keys(), key=(lambda key: msds[key]))
    feature_subset.append(max_msd[0])
    feature_subset.append(max_msd[1])
    G.remove_node(max_msd[0])
    G.remove_node(max_msd[1])

# TODO: Implement itung variance of relevance (u/ nodes_var) pas initialize graph
# TODO: uncomment mpt()
# def mpt():
#   for _ in range(MAX_FEATURE_SUBSET):
#     mpt = {}
#     nodes = nx.get_node_attributes(G, 'relevance')
#     nodes_var = nx.get_node_attributes(G, 'var_of_rel')
#     for key1, value in nodes.items():
#       diff_score = 0
#       for key2 in feature_subset:
#         diff_score = diff_score + (math.sqrt(nodes_var[key2]) * G[key1][key2]['similarity'])
#       mpt[key1] = value - (TRADE_OFF * nodes_var[key1] + 2 * TRADE_OFF * math.sqrt(nodes_var[key1]) * diff_score)
#     max_rel = max(mpt.keys(), key=(lambda key: mpt[key]))
#     feature_subset[max_rel] = mpt[max_rel]
#     G.remove_node(max_rel)

if __name__ == "__main__":
  print('starting feature selection using diversification method...')
  arg = 'msd'
  try:
    arg = sys.argv[1]
  except IndexError:
    print('set `msd` as default argument...')
  # read Graph
  G = nx.read_gexf(GRAPH_PATH)
  G = nx.relabel_nodes(G, lambda x: int(x))
  feature_subset = []

  if (arg == 'mmr'):
    mmr()
  elif (arg == 'msd'):
    msd()
  # elif (arg == 'mpt'):
  #   mpt()

  # change nodes index to feature id
  feature_subset = [i + 1 for i in feature_subset]

  n_subset = 5
  while n_subset < MAX_FEATURE_SUBSET:
    fileHandle = open("/results/" + arg + "/sub" + str(n_subset) + ".txt", "w+")
    for i in range(n_subset):
      fileHandle.write("%d\n" % feature_subset[i])
    fileHandle.close()

  fileHandle = open("/results/" + arg + "/sub" + str(MAX_FEATURE_SUBSET) + ".txt", "w+")
  for i in range(MAX_FEATURE_SUBSET):
    fileHandle.write("%d\n" % feature_subset[i])
  fileHandle.close()
