possible = {
  'dairy': { 'abc' },
  'eggs': { 'abc', 'def' },
  'fish': { 'abc', 'def', 'ghi' },
}

def reduce(possible):
  reduced = {}
  singles = set()

  while len(reduced) != len(possible):
    for k, v in possible.items():
      if len(v - singles) == 1:
        v = list(v)[0]
        reduced[k] = v
        singles.add(v)

  return reduced

print(reduce(possible))
