import os
import sys
import time
import utils

debug = False


def extend(clauses, x):
   return [[x]] + [c.copy() for c in clauses]


def unit_propagation(clauses):
  result = False
  while True:
    modified = False
    for clause in clauses:
      if len(clause) == 1:
        x = clause[0]
        for j in reversed(range(len(clauses))):
          if x in clauses[j]:
            del clauses[j]
            modified = True
          elif -x in clauses[j]:
            clauses[j].remove(-x)
            modified = True
    if modified:
      result = True
    else:
      return result


def pure_literal(clauses):
  result = False
  positive = set()
  negative = set()
  for clause in clauses:
    for x in clause:
      if x > 0:
        positive.add(x)
      else:
        negative.add(-x)
  for x in positive - negative:
    for i in reversed(range(len(clauses))):
      if x in clauses[i]:
        del clauses[i]
        result = True
  for x in negative - positive:
    for i in reversed(range(len(clauses))):
      if -x in clauses[i]:
        del clauses[i]
        result = True
  return result


def solve(clauses):
  if debug:
    print("c solving clauses", clauses)
  result = unit_propagation(clauses)
  if debug and result:
    print("c Unit propagation")
  result = pure_literal(clauses)
  if debug and result:
    print("c Pure literal")

  for clause in clauses:
    if len(clause) == 0:
      if debug:
        print("c1 False clauses", clauses)
      return False
  if len(clauses) == 0:
    if debug:
      print("c1 True clauses", clauses)
    return True

  x = clauses[0][0]
  if debug:
    print("c Extend clauses", clauses, "with", [x])
  result = solve(extend(clauses, x))
  if not result:
    if debug:
      print("c Extend clauses", clauses, "with", [-x])
    result = solve(extend(clauses, -x))
  if debug:
    print("c2", result, "clauses", clauses)
  return result

def dpll(file):
  clauses = utils.parse_cnf(file)
  print('c Solving system from {0} with {1} clauses'.format(file, len(clauses)))

  clauses = [list(clause) for clause in clauses]
  start = time.perf_counter()
  result = solve(clauses)
  elapsed = time.perf_counter() - start
  print("s SATISFIABLE" if result else "s UNSATISFIABLE")
  print(f'Solved in: {elapsed:.6f} seconds')
  return elapsed


if __name__ == '__main__':
  if len(sys.argv) == 2:
    dpll(sys.argv[1])
  else:
    dir_groups = ['uf5-23', 'uf10-45', 'uf20-91', 'uf75-325', 'uf100-450', 'uf150-675', 'uf200-900']
    results = {}
    for dirname in dir_groups:
      dir = "examples/{0}".format(dirname)
      count = 0
      total_time = 0
      for file in sorted(os.listdir(dir)):
        total_time = total_time + dpll("{0}/{1}".format(dir, file))
        count = count + 1
      results[dir] = total_time / count
    print("Results:")
    print(results)
