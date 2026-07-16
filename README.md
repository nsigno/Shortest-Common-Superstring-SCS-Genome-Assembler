# Shortest Common Superstring (SCS) Genome Assembler

Modular Python DNA assembler that reconstructs a superstring of DNA extracted from a FASTA file using graph theory and no additional libraries.

## Project Overview
The project is modeled as an asymmetric TSP, using a dummy node to convert a linear path into a cycle
A path represents the order in which strings must be assembled to form the superstring, and the optimal TSP path corresponds to the SCS.
- `dna_processing` contains the functions needed to convert a FASTA file into a DNA array and to make an adjacency matrix based on the suffix-prefix overlap length.
- `tsp_solver` contains a general solver for the ATSP problem modified to remove the dummy node and get a path.

### Main Algorithms
- Nearest neighbour (closest node search) is a heuristic used to find an initial upper bound to prune suboptimal solutions.
- MST Relaxation (calculated using Kruskal's algorithm) is a relaxation used to find lower bounds.
- Branch and Bound (BnB) engine uses the heuristic and relaxation to explore only promising nodes of the decision tree and drastically reduce the exponential time complexity of the ATSP problem.
- The modular structure of the project allows for the future implementation of better heuristics and relaxations to get a more aggressive BnB search (more advanced algorithms were outside the scope of the project).

## Repo Structure
```text
your-project-name/
│
├── dna_processing/
│   ├── __init__.py
│   ├── fasta_reader.py    
│   └── string_overlap.py    
│
├── tsp_solver/
│   ├── __init__.py
│   ├── heuristics.py      
│   ├── relaxations.py      
│   └── engine.py         
│
├── main.py                  
└── README.md
```

## Getting started

- Python 3.10 or higher is required, no external dependencies are needed.
- To run the assembler, pass the path of a FASTA file as a command-line argument.
- The superstring will be saved to `output.txt`.
