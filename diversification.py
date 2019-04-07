import sys
import networkx as nx

NODE_SIZE = 136
NDCG_PATH = '/home/vigor/Documents/TA/NDCGs/'
RANKS_PATH = '/home/vigor/Documents/TA/ranks/'

def mmr():
  print('using MMR')

def msd():
  print('using MSD')

def mpt():
  print('using MPT')

def init_relevance():
  for i in range(0,136):
    relFile = open(NDCG_PATH+'NDCG'+str(i+1)+'.txt')
    lineList = relFile.readlines()
    relFile.close()
    G.nodes[i]['relevance'] = float(lineList[-3][22:-1])

def init_similarity():
  print('test')

if __name__ == "__main__":
  print('starting feature selection using diversification method...')
  arg = 'msd'
  try:
    arg = sys.argv[1]
  except IndexError:
    print('set `msd` as default argument...')
  G = nx.complete_graph(NODE_SIZE)
  init_relevance()
  init_similarity()

  if (arg == 'mmr'):
    mmr()
  elif (arg == 'msd'):
    msd()
  elif (arg == 'mpt'):
    mpt()
