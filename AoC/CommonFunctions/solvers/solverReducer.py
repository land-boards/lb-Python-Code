possible = {
  'dairy': { 'abc' },
  'eggs': { 'abc', 'def' },
  'fish': { 'abc', 'def', 'ghi' },
}

def reduce(possible):
  reduced = {}

  while len(reduced) != len(possible):
    for k, v in possible.items():
      single = v - set(reduced.values())

      if len(single) == 1:
        reduced[k] = list(single)[0]

  return reduced

print(reduce(possible))
