from random import randint
import sys
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
  if fr:
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
      k = randint(i,n-1)
      initSwap(k,i)
  return n-j

def stringify():
  return "\n".join(["".join(['Q' if j == q else '.' 
          for j in range(n)]) for q in queens])+'\n'

def repair(rem,fr,steps):
  s = 0
  for i in range(n-rem,n):
    if i!=fr and isAttacked(i):
      while True:
        if s == steps: return False
        j = randint(0,n-1)
        if j not in [i,fr]:
          s += 1; swap(i,j)
          if isAttacked(i) or isAttacked(j): swap(i,j)
          else: break
  return True

def solver(size,fixed=(None,None)):
  global ndiags, pdiags, n
  n = size; its = 0
  if n == 1: return "Q\n"
  if n in {2,3}: return None
  while its < 100:
    ndiags = (2*n-1)*[0]; pdiags = (2*n-1)*[0]
    rem = getQueens(*fixed); its += 1
    solution = repair(rem,fixed[0],2*n) 
    if solution: return stringify()
  return None

if __name__ == "__main__":
  if len(sys.argv) == 2:
      print(solver(int(sys.argv[1])))
  elif len(sys.argv) == 3:
      fx,fy = sys.argv[2].strip('[]').split(',')
      print(solver(int(sys.argv[1]),(int(fx),int(fy))))
  else:
    raise ValueError("Incorrect input") 
  