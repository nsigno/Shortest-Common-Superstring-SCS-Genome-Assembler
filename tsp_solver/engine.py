from relaxations import find, union, costr_adj_heap, kruskal_mst

# node class used to represent states for the BnB tree

class Node():
  def __init__(self, in_edges=None, out_edges=None):
      self.in_edges : set[tuple[int,int]] = set(in_edges) if in_edges is not None else set()
      self.out_edges : set[tuple[int,int]] = set(out_edges) if out_edges is not None else set()


class TspBnBSolver:
  def __init__(self, matrix : list[list[int]], initial_cost : int | float, initial_tour : list[int]):
    self.matrix : list[list[int]] = matrix
    self.num_nodes : int = len(matrix)
    self.best_cost : int|float = initial_cost
    self.best_tour : list[int] = initial_tour

    #initialises startup values
    self.adj_heap : list[tuple[int, int, int]] = costr_adj_heap(matrix)
    self.matrix_min : int | float = float('inf')
    for el in matrix:
      self.matrix_min = min(self.matrix_min, min(el))
    

  def solve(self) -> tuple[int | float, list[int]]:

    root_node = Node()
    stack : list[Node] = [root_node]

    while(stack):

      curr_node = stack.pop()

      # if the node has invalid in_edges it gets skipped immediately
      if not self.is_feasible(curr_node) : continue

      mst_cost, mst_edges = kruskal_mst(self.adj_heap, self.num_nodes, curr_node.in_edges, curr_node.out_edges, self.matrix, self.matrix_min)
      LB = mst_cost + (self.num_nodes-1)*(self.matrix_min-1)

      # if the best solution is worse than the best cost found it gets skipped
      if LB>=self.best_cost: continue

      # if the solution is a valid tsp solution it gets processed
      if len(curr_node.in_edges) == self.num_nodes - 1:
        self.process_leaf_node(curr_node)
        continue
  
      # adds branches of node to the stack
      for child in self.create_branches(curr_node, mst_edges):
        stack.append(child)
    return self.best_cost, self.best_tour
  
  # checks if a collection of in_edges is valid: 
  # every graph node can't have more than 2 edges and there must be no cycles
  def is_feasible(self, node:Node) -> bool:
    degree : list[int] = [0]* self.num_nodes

    # checks edges
    for u,v in node.in_edges:
      degree[u]+=1
      degree[v]+=1

    for g in degree:
      if g > 2:
          return False
  
    # checks for cycles
    parent = [i for i in range(self.num_nodes)]
    for u,v in node.in_edges:
      root_u = find(parent, u)
      root_v = find(parent,v)

      if root_u == root_v:
        return False
      else: union(parent, u, v)
    return True



  def process_leaf_node(self, node: Node) :

    degree : list[int] = [0] * self.num_nodes

    #sets degree of each node
    for u, v in node.in_edges:
        degree[u] += 1
        degree[v] += 1
    
    # if there are more than 2 edges the solution isn't a valid path
    edges = [i for i, g in enumerate(degree) if g == 1]
    if len(edges) != 2:
        return
    
    # if the arc connecting the 2 edges is in out_edges the solution isn't valid
    arc = (min(edges[0], edges[1]), max(edges[0], edges[1]))
    if arc in node.out_edges:
        return
    
    # finds the 2 arcs that connect the dummy node
    best_tour_test = node.in_edges.union({arc})
    dummy_nodes = []
    for u, v in best_tour_test:
        if u == self.num_nodes - 1 or v == self.num_nodes - 1:
            dummy_nodes.append((min(u, v), max(u, v)))

    # removes the dummy nodes to form a valid path and finds the ends of that path
    ends = []
    best_tour_test_clean = set(best_tour_test)
    for i in dummy_nodes:
        best_tour_test_clean.discard(i)
        for j in i:
            if j != self.num_nodes - 1:
                ends.append(j)

    # builds a path (list of matrix nodes) by following edges from one end to the other
    path = [ends[0]]
    current_node = ends[0]
    while current_node != ends[1]:
      found_arc = next(a for a in best_tour_test_clean if current_node in a)
      next_node = found_arc[1] if current_node == found_arc[0] else found_arc[0]
      path.append(next_node)
      best_tour_test_clean.discard((min(current_node, next_node), max(current_node, next_node)))
      current_node = next_node

    # finds the cost of following the path both ways: the real cost is the min of the 2
    path_cost = sum(self.matrix[path[i]][path[i+1]] for i in range(len(path)-1))
    back_path_cost = sum(self.matrix[path[i+1]][path[i]] for i in range(len(path)-1))
    real_cost = min(path_cost, back_path_cost)

    # if the real cost is better than the best cost found we have a better tsp solution candidate
    # the current solution is updated
    if real_cost < self.best_cost:
      self.best_cost = real_cost
      self.best_tour = path if path_cost < back_path_cost else path[::-1]


  # finds an edge from the mst that isn't in in_edges or out_edges, creates 2 BnB nodes adding the edge to each set
  def create_branches(self, node: Node, mst_edges: set[tuple[int, int]]) -> list[Node]:
    for el in mst_edges:
          if el not in node.in_edges and el not in node.out_edges:

              out_node = Node(node.in_edges, node.out_edges)
              out_node.out_edges.add(el)

              in_node = Node(node.in_edges, node.out_edges)
              in_node.in_edges.add(el)
              
              return [out_node, in_node]
    return []