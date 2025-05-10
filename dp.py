import os
import sys
import time
import utils

debug = False

def unit_propagation(clauses):
  result = False
  while True:
    modified = False
    for clause in clauses:
      if len(clause) == 1:
        x = list(clause)[0]
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


def resolvent(clause1, clause2):
  for literal1 in clause1:
    literal2 = -literal1
    if literal2 in clause2:
      c1 = clause1 - { literal1 }
      c2 = clause2 - { literal2 }
      if len(c1 & { -l for l in c2 }) > 0:  # Tautology
        return None
      return c1 | c2
  return None


def solve(clauses):
  unit_propagation(clauses)
  pure_literal(clauses)
  while len(clauses):
    unit_propagation(clauses)

    for clause in clauses:
      if len(clause) == 0:
        return False

    new_clauses = False
    for clause1 in clauses:
      for clause2 in clauses:
        if clause1 == clause2:
          continue
        r = resolvent(clause1, clause2)
        if r is None or r in clauses:
          continue
        if len(r) == 0:
          return False
        utils.add_clause(clauses, r)
        if debug:
          print("c Add resolvent", r, 'for', clause1, 'and', clause2)
        new_clauses = True
    if not new_clauses:
      return True
    

def dp(file):
  clauses = utils.parse_cnf(file)
  print('c Solving system from {0} with {1} clauses'.format(file, len(clauses)))

  start = time.perf_counter()
  result = solve(clauses)
  elapsed = time.perf_counter() - start
  print("s SATISFIABLE" if result else "s UNSATISFIABLE")
  print(f'Solved in: {elapsed:.6f} seconds')
  return elapsed


if __name__ == '__main__':
  if len(sys.argv) == 2:
    dp(sys.argv[1])
  else:
    dir_groups = ['uf5-23', 'uf6-27', 'uf7-32', 'uf8-36']
    results = {}
    for dirname in dir_groups:
      dir = "examples/{0}".format(dirname)
      count = 0
      total_time = 0
      for file in sorted(os.listdir(dir)):
        total_time = total_time + dp("{0}/{1}".format(dir, file))
        count = count + 1
      results[dir] = total_time / count
    print("Results:")
    print(results)
