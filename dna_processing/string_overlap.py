
# gets the length of the longest suffix of t that is equal to the prefix of s

def get_suf_length(f:str, s:str) -> int:
  for i in range(min(len(f), len(s)), 0, -1):
    if f.endswith(s[:i]):
        return i
  return 0


# builds an adjacency matrix where the arcs have the (negative) length from get_suf_length

def costr_adj_matrix(num_nodi:int, dna_arr:list[str])-> list[list[int]]:
  matrix: list[list[int]] = [[0] * (num_nodi) for _ in range(num_nodi)]
  for i in range(num_nodi-1): 
    for j in range(num_nodi-1):
      if i==j: matrix[i][j]=1
      else: matrix[i][j] = get_suf_length(dna_arr[i], dna_arr[j])*(-1)
  return matrix