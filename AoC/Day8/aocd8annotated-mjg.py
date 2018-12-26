
values = [
  2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2
]

def md_sum(node):
  return sum(node[1]) + sum(map(md_sum, node[0]))

# Node can be thought of as [[Nodes], [Metadata]]

# Returns [Node, [Int]] --- current parse and remaining numbers
def parse_node(text):
  print 'parse_node', text
  n_children = text[0]
  n_metadata = text[1]
  remainder = text[2:]
  children = []

  for _ in xrange(n_children):
    parse_result = parse_node(remainder)
    child = parse_result[0]
    remainder = parse_result[1]
    children.append(child)

  print 'done parsing children at', text
  return [[children, remainder[:n_metadata]], remainder[n_metadata:]]

print md_sum(parse_node(values)[0])