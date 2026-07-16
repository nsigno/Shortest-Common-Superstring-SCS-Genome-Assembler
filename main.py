import argparse
from dna_processing.fasta_reader import dna_from_fasta
from dna_processing.string_overlap import costr_adj_matrix, get_suf_length
from tsp_solver.heuristics import closest_node_search
from tsp_solver.engine import TspBnBSolver

OUTPUT_FILENAME = "output.txt"

def main():
  parser = argparse.ArgumentParser(
        description="Shortest Common Superstring genome assembler"
    )
  
  parser.add_argument(
        "fasta_path", 
        type=str, 
        help=".txt or .fasta file path containing fasta format dna reads"
    )
  
  args = parser.parse_args()  

  dna_arr : list[str] = []

  dna_from_fasta(args.fasta_path, dna_arr)

  num_nodi = len(dna_arr)+1

  matrix = costr_adj_matrix(num_nodi, dna_arr)

  upper_bound, best_tour = closest_node_search(matrix)

  solver = TspBnBSolver(matrix, upper_bound, best_tour)
  
  best_tour = solver.solve()[1]

  superstring = dna_arr[best_tour[0]]
  for i in range(1, len(best_tour)):
    next_read = dna_arr[best_tour[i]]
    superstring += next_read[get_suf_length(superstring, next_read):]

  with open(OUTPUT_FILENAME, "w") as f:
      f.write(superstring)



if __name__ == "__main__":
    main()