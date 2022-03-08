from random import randint
import sys, os
from time import perf_counter
n = ndiags = pdiags = queens = None

def isAttacked(j):
  y = queens[j]
  return pdiags[y+j] > 1 or ndiags[n+j-y-1] > 1

def swap(i,j):
  y = queens[i]; z = queens[j]
  ndiags[n+i-y-1] -=1; pdiags[i+y] -=1
  ndiags[n+j-z-1] -=1; pdiags[j+z] -=1
  ndiags[n+i-z-1] +=1; pdiags[i+z] +=1
  ndiags[n+j-y-1] +=1; pdiags[j+y] +=1
  queens[i],queens[j] = queens[j],queens[i]

def initSwap(i,j):
  queens[i],queens[j] = queens[j],queens[i]
  y = queens[j]; pdiags[y+j] +=1; ndiags[n+j-y-1] +=1

def undoInitSwap(i,j):
  y = queens[j]; pdiags[y+j] -=1; ndiags[n+j-y-1] -=1
  queens[i],queens[j] = queens[j],queens[i]
  
def getQueens(fr,fc):
  global queens
  queens, j = [i for i in range(n) if i != fc], 0
  if fr != None:
    queens.insert(fr,fc)
    ndiags[n+fr-fc-1] += 1; pdiags[fr+fc] += 1
  for _ in range(3*n):
    if j == fr: j += 1
    if j == n: break
    k = randint(j,n-1)
    if k not in [j,fr]:
      initSwap(k,j)
      if not isAttacked(j): j += 1
      else: undoInitSwap(k,j)
  for i in range(j,n):
    if i != fr:
      while True:
        k = randint(i,n-1)
        if k != fr: break
      initSwap(k,i)
  return n-j

def stringify():
  out = '['
  for i,q in enumerate(queens):
    out += str(q)
    if i<n-1: out += ',' if not i or i%25 else '\n'
  return out + ']'

def repair(rem,fr,steps):
  s = 0
  for i in range(n-rem,n):
    if i!=fr and isAttacked(i):
      while True:
        if s == steps: return False
        j = randint(0,n-1)
        if j not in {i,fr}:
          s += 1; swap(i,j)
          if isAttacked(i) or isAttacked(j): swap(i,j)
          else: break
  return True

def solver(size,fixed=(None,None)):
  global ndiags, pdiags, n
  n = size; its = 0
  if n == 1: return "Q\n"
  if n < 4: return None
  while its < 100:
    ndiags = (2*n-1)*[0]; pdiags = (2*n-1)*[0]
    rem = getQueens(*fixed); its += 1
    solution = repair(rem,fixed[0],2*n) 
    if solution: return stringify()
  return None

def getFileNumber(path):
  files = os.listdir(path)
  if files:
    for idx,file in enumerate(files):
      files[idx] = int(file[:-4])
    files.sort()
    return 1 + files.pop()
  return 1

if __name__ == "__main__":
  if len(sys.argv) == 2:
    start = perf_counter()
    qns = solver(int(sys.argv[1]))
    end = perf_counter()
    info = (f"\n====<<  Solution for {sys.argv[1]}-queens  >>====\n\n"
          + f"Execution time: {end-start:.3f}\n\n")
  elif len(sys.argv) == 3:
    fx,fy = sys.argv[2].strip('[]').split(',')
    start = perf_counter()
    qns = solver(int(sys.argv[1]),(int(fx),int(fy)))
    end = perf_counter()
    info = (f"\n====<<  Solution for {sys.argv[1]}-queens with" 
          + f" fixed location ({fx},{fy})  >>====\n\n"
          + f"Execution time: {end-start:.3f}\n\n")
  else:
    raise ValueError("Incorrect input") 

  path = os.getcwd() + "/output"
  if not os.path.exists(path): 
    os.makedirs(path)
	
  board = "\n".join(["".join(['Q' if j == q else '.' 
          for j in range(n)]) for q in queens])+'\n\n' 
  fileNum = getFileNumber(path)
  outFile = path + f"/{fileNum}.out"
  output = info  + 'Queen positions:\n\n' + qns
  if n < 200: output += '\n\n>> Chessboard <<\n\n' + board
	
  with open(outFile, 'w', encoding = "utf-8") as f:
    f.write(output)
  