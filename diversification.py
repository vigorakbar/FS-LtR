import sys
import networkx as nx

GRAPH_PATH = '/home/vigor/Documents/TA/graph/'

def mmr():
  print('using MMR')

def msd():
  print('using MSD')

def mpt():
  print('using MPT')

if __name__ == "__main__":
  print('starting feature selection using diversification method...')
  arg = 'msd'
  try:
    arg = sys.argv[1]
  except IndexError:
    print('set `msd` as default argument...')
  # read Graph
  G = nx.read_gexf(GRAPH_PATH)

  if (arg == 'mmr'):
    mmr()
  elif (arg == 'msd'):
    msd()
  elif (arg == 'mpt'):
    mpt()
