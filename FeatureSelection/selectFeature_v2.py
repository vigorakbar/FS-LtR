import sys
import networkx as nx
import math

pathFile = open('path.txt')
linePath = pathFile.readlines()
pathFile.close()

GRAPH_PATH = linePath[3][:-1]
MAX_FEATURE_SUBSET = 75
TRADE_OFF = 0.5
XGAS_P = 0.5

def mmr():
  edges = nx.get_edge_attributes(G, 'similarity')
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

def ngas():
  nodes = nx.get_node_attributes(G, 'relevance')
  edges = nx.get_edge_attributes(G, 'similarity')
  max_rel = max(nodes.keys(), key=(lambda key: nodes[key]))
  feature_subset.append(max_rel)
  G.remove_node(max_rel)
  for _ in range(1, MAX_FEATURE_SUBSET):
    vl_dict = {x: y for x,y in edges.items() if max_rel in x}
    vl = min(vl_dict.keys(), key=(lambda key: vl_dict[key]))
    vl = (vl[0] if vl[1] == max_rel else vl[1])
    edges = nx.get_edge_attributes(G, 'similarity')
    vh_dict = {x: y for x,y in edges.items() if vl in x}
    vh = max(vh_dict.keys(), key=(lambda key: vh_dict[key]))
    vh = (vh[0] if vh[1] == vl else vh[1])
    vlvh = {vl: G.nodes[vl]['relevance'], vh: G.nodes[vh]['relevance']}
    max_rel = max(vlvh.keys(), key=(lambda key:vlvh[key]))
    feature_subset.append(max_rel)
    G.remove_node(max_rel)

def xgas():
  nodes = nx.get_node_attributes(G, 'relevance')
  edges = nx.get_edge_attributes(G, 'similarity')
  max_rel = max(nodes.keys(), key=(lambda key: nodes[key]))
  feature_subset.append(max_rel)
  G.remove_node(max_rel)
  for _ in range(1, MAX_FEATURE_SUBSET):
    edges_temp = {x: y for x,y in edges.items() if max_rel in x}
    sub_edge = {}
    edges = nx.get_edge_attributes(G, 'similarity')
    for _ in range(math.ceil(len(G)*XGAS_P)):
      min_sim_key = min(edges_temp.keys(), key=(lambda key: edges_temp[key]))
      min_sim = (min_sim_key[0] if min_sim_key[1] == max_rel else min_sim_key[1])
      sub_edge[min_sim] = nodes[min_sim]
      del edges_temp[min_sim_key]
    max_rel = max(sub_edge.keys(), key=(lambda key: sub_edge[key]))
    feature_subset.append(max_rel)
    G.remove_node(max_rel)

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
    print("using mmr...")
    mmr()
  elif (arg == 'msd'):
    print("using msd...")
    msd()
  # elif (arg == 'mpt'):
  #   print("using mpt...")
  #   mpt()
  elif (arg == 'ngas'):
    print("using ngas...")
    ngas()
  elif (arg == 'xgas'):
    print("using xgas...")
    xgas()
  # elif (arg == 'hcas'):
  #   print("using hcas...")
  #   hcas()

  # change nodes index to feature id
  feature_subset = [i + 1 for i in feature_subset]

  n_subset = 5
  while n_subset < MAX_FEATURE_SUBSET:
    fileHandle = open("results/" + arg + "_v2/sub" + str(n_subset) + ".txt", "w+")
    sorted_subset = feature_subset[:n_subset]
    sorted_subset.sort()
    for i in range(n_subset):
      fileHandle.write("%d\n" % sorted_subset[i])
    fileHandle.close()
    n_subset += 5

  fileHandle = open("results/" + arg + "_v2/sub" + str(MAX_FEATURE_SUBSET) + ".txt", "w+")
  feature_subset.sort()
  for i in range(MAX_FEATURE_SUBSET):
    fileHandle.write("%d\n" % feature_subset[i])
  fileHandle.close()

  print("done.")
