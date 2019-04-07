import sys

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

  
  if (arg == 'mmr'):
    mmr()
  elif (arg == 'msd'):
    msd()
  elif (arg == 'mpt'):
    mpt()
