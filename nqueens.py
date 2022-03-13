#  ┌─────────────────────────────────────────────────────────┐
#  │  File name: nqueens.py                                  │
#  │  Author: David De Potter, pl3onasm@gmail.com            │
#  │  License: refer to the license file in this repository  │
#  │  Description: this module makes sure that the output    │
#  │  generated by the solver is nicely formatted and stored │ 
#  └─────────────────────────────────────────────────────────┘

import sys, os; from time import perf_counter
from solver import *

def getFileNumber(path):
  files = os.listdir(path)
  if files:
    for idx,file in enumerate(files):
      files[idx] = int(file.split('.')[0])
    files.sort()
    return 1 + files.pop()
  return 1

def stringify(n,queens):
  out = '['
  for i,q in enumerate(queens):
    out += str(q)
    if i<n-1: out += ',' if not i or i%25 else '\n'
  return out + ']\n'

def main(n,fixed=(None,None)):
  if not fixed[0]:
    start = perf_counter()
    sol = solver(n,fixed)
    end = perf_counter()
    info = (f"\n====<<  Solution for {sys.argv[1]}-queens  >>====\n\n"
          + f"Execution time: {end-start:.3f} s\n\n")
  else:
    fx,fy = sys.argv[2].strip('[]').split(',')
    start = perf_counter()
    sol = solver(n,fixed)
    end = perf_counter()
    info = (f"\n====<<  Solution for {sys.argv[1]}-queens with" 
          + f" fixed location ({fx},{fy})  >>====\n\n"
          + f"Execution time: {end-start:.3f} s\n\n")

  path = os.getcwd() + "/output"
  if not os.path.exists(path): 
    os.makedirs(path)
  outFile = path + f"/{getFileNumber(path)}.out"

  if sol:
    output = info  + 'Queen positions:\n\n' + stringify(n,sol)
    if n < 200: 
      board = "\n".join(["".join(['Q' if j == q else '.' 
          for j in range(n)]) for q in sol])+'\n\n' 
      output += '\n>> Chessboard <<\n\n' + board
  else:
    output = info + "\nThere is no solution for the given problem.\n\n"
	
  with open(outFile, 'w', encoding = "utf-8") as f:
    f.write(output)

if __name__ == "__main__":
  if len(sys.argv) == 2:
    main(int(sys.argv[1]))
  elif len(sys.argv) == 3:
    fx,fy = sys.argv[2].strip('[]').split(',')
    main(int(sys.argv[1]),(int(fx),int(fy)))
  else:
    raise ValueError("Incorrect input") 