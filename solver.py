#  ┌─────────────────────────────────────────────────────────┐
#  │  File name: solver.py                                   │
#  │  Author: David De Potter, pl3onasm@gmail.com            │
#  │  License: refer to the license file in this repository  │
#  │  Description: computes a solution for a given size of   │
#  │  the n-qeens problem, either with or without one fixed  │
#  │  queen position, using an iterated local search algo-   │
#  │  rithm guided by a minimal conflicts heuristic          │
#  └─────────────────────────────────────────────────────────┘

from random import randint
n = ndiags = pdiags = queens = None

def isAttacked(j):
  y = queens[j]
  return pdiags[y+j] > 1 or ndiags[n+j-y-1] > 1

def swap(i,j):
  y = queens[i]; z = queens[j]
  ndiags[n+i-y-1] -=1; pdiags[i+y] -=1; pdiags[j+y] +=1
  ndiags[n+j-z-1] -=1; pdiags[j+z] -=1; pdiags[i+z] +=1
  ndiags[n+j-y-1] +=1; ndiags[n+i-z-1] +=1; 
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
    if k not in {j,fr}:
      initSwap(k,j)
      if not isAttacked(j): j += 1
      else:  undoInitSwap(k,j)
  for i in range(j,n):
    if i != fr:
      while True:
        k = randint(i,n-1)
        if k != fr: break
      initSwap(k,i)
  return n-j

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

def solver(size,fixed):
  global ndiags, pdiags, n
  n = size; its = 0
  if n == 1: return "Q\n"
  if n < 4: return None
  while its < 100:
    ndiags = (2*n-1)*[0]; pdiags = (2*n-1)*[0]
    rem = getQueens(*fixed); its += 1 
    if repair(rem,fixed[0],3*n): return queens
  return None