from mpi4py import MPI

serial = 8868

comm = MPI.COMM_WORLD
MPsize = comm.Get_size()
MPrank = comm.Get_rank()

def power((x, y)):
  return ((x + 10) * ((x + 10) * y + serial)) / 100 % 10 - 5

def ridge((x, y), size):
  yield (x+size-1, y+size-1)

  for i in xrange(0, size-1):
    yield (x + i, y + size - 1)
    yield (x + size - 1, y + i)

def max_expand_from((x, y)):
  def aux(acc, best, best_size, size):
    if 300 - size - x <= 0 or 300 - size - y <= 0:
      return (best, best_size)

    newSum = acc + sum(power(pt) for pt in ridge((x, y), size))

    if newSum > best:
      return aux(newSum, newSum, size, size + 1)

    return aux(newSum, best, best_size, size + 1)

  start = power((x, y))

  return (aux(start, start, 1, 2), (x, y))

my_best = None

for x in xrange(MPrank, 301, MPsize):
  for y in xrange(1, 301):
    current_best = max_expand_from((x, y))

    if not my_best or current_best[0][0] > my_best[0][0]:
      my_best = current_best

answers = comm.gather(my_best,root=0)
best = None

if MPrank == 0:
  for answer in answers:
    if not best or answer[0][0] > best[0][0]:
      best = answer

print best
