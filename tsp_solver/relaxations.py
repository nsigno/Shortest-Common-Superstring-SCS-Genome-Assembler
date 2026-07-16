# heap operations:


def heap_insert(heap:list[tuple[int,int,int]], el:tuple[int,int,int]):
  heap.append(el)
  i : int = len(heap)-1
  while(i!=0):
    parent : int = ((i-1)//2)
    if heap[i] < heap[parent]:
      heap[i], heap[parent] = heap[parent], heap[i]
      i = parent
    else: break
  return


def smallest_heapify(heap:list[tuple[int,int,int]], i:int):
  l : int = i*2+1
  r : int = (i*2)+2
  if l < len(heap) and heap[l] < heap [i]:
    smallest : tuple[int, int, int]= l
  else: smallest = i
  if r < len(heap) and heap[r] < heap[smallest]:
    smallest : tuple[int, int, int] = r
  if smallest != i:
    heap[i], heap[smallest] = heap[smallest], heap[i]
    smallest_heapify(heap, smallest)


def heap_extract_smallest(heap:list[tuple[int, int, int]])-> tuple[int, int, int]:
  smallest : tuple[int, int, int] = heap[0]
  if len(heap)==1 : heap.pop()
  else: 
    heap[0] = heap.pop()
    smallest_heapify(heap, 0)
  return smallest


def costr_adj_heap(matrix : list[list[int]])-> list[tuple[int,int,int]]:
  adjHeap : list[tuple[int,int,int]] = []
  smallest : int | float = float('inf')
  for el in matrix: smallest = min(smallest, min(el)) 

  for i in range(len(matrix)):
    for j in range(i+1, len(matrix)):
      heap_insert(adjHeap, (min(matrix[i][j],matrix[j][i])-smallest+1, min(i,j), max(i,j)))
  return adjHeap


# kruskal operations:


def find(parent : list[int], i : int)-> int:
  if parent[i] == i: return parent[i]
  else: parent[i] = find(parent, parent[i])
  return parent[i]


def union(parent : list[int], i : int, j : int):
  radice_i : int = find(parent, i)
  radice_j : int = find(parent, j)
  parent[radice_i] = radice_j


# main function:


def kruskal_mst(adjHeap : list[tuple[int, int, int]], num_nodi : int, in_edges : set[tuple[int, int]], out_edges : set[tuple[int, int]], matrix : list[list[int]], smallest : int) -> tuple[int,set[tuple[int, int]]]:
  parent : list[int] = [i for i in range(num_nodi)]
  mst_cost : int = 0
  mst_count : int = 0
  mst_edges : set = set()

  # adds edges of in_edges to the tree before building the mst
  for u,v in in_edges:
    union(parent, u, v) 
    mst_cost += min(matrix[u][v], matrix[v][u])-smallest+1
    mst_count += 1
    mst_edges.add((u,v))

  heap : list[tuple[int, int, int]]= adjHeap.copy()

  # finds the shortest edge using the heap, if it's not in out_edges and doesn't form a cycle it gets added to the mst
  while heap and mst_count < num_nodi -1: 
    el : tuple[int, int, int]= heap_extract_smallest(heap)
    
    if((min(el[1],el[2]), max(el[1], el[2])) in out_edges): continue

    if (find(parent, el[1])!=find(parent, el[2])):
      union(parent, el[1], el[2])
      mst_cost += el[0]
      mst_count += 1
      mst_edges.add((min(el[1],el[2]), max(el[1], el[2])))

  if mst_count < num_nodi-1: return float('inf'), set()
  return (mst_cost, mst_edges)