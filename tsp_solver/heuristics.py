
# simple nearest neighbour search for tsp heuristic

def closest_node_search(matrix:list[list[int]])->tuple[int, list[int]]:
  i : int = 0
  length = 0
  L : list[int] = [0]
  while (len(L)<len(matrix)-1):
    smallest : int = min([(item, idx) for idx, item in enumerate(matrix[i]) if idx not in L and idx != len(matrix)-1])
    length += smallest[0]
    L.append(smallest[1])
    i=smallest[1]

  return length, L