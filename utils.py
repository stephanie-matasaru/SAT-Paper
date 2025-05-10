from bisect import bisect
import sys

def add_clause(clauses, clause):
  try:
    index = -1 - clauses.index(clause)
  except ValueError:
    index = len(clauses)
    clauses.append(clause)
  return index

def parse_cnf(filename):
  clauses = []
  nbclauses = 0
  index = 0
  with open(filename, 'r') as file:
    # Read each line in the file
    for line in file:
      line = line.strip()
      if line.startswith('c'):
        continue
      if line.startswith('p'):
        parts = line.split()
        if parts[0] != "p" or parts[1] != "cnf":
          sys.exit(1)
        nbclauses = int(parts[3])
      else:
        i = add_clause(clauses, set([int(num) for num in line.split()[:-1]]))
        if i < 0:
          print("c Clause", index, 'is duplicate of clause', -i - 1)
        index = index + 1
        if index == nbclauses:
          break
  return clauses
