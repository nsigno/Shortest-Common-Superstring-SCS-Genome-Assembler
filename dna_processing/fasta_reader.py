import os

# simple reader that converts a fasta file in an array of dna genomas (and tags if needed)

def dna_from_fasta(path : str, target : list[str] | list[list[str]], tags : bool = False):
  if not os.path.exists(path):
        raise FileNotFoundError(f"file {path} non existent")
  
  with open(path, 'r') as f:
    first_line = ""
    for line in f:
        stripped = line.strip()
        if stripped: 
            first_line = stripped
            break
    
    if not first_line:
        raise ValueError(f"file {path} empty")
        
    if not first_line.startswith('>'):
        raise ValueError(f"file not in valid FASTA format")

    f.seek(0)
    
    dna = ""
    tag = ""
    
    for line in f:
        stripped_line = line.strip()
        if not stripped_line:
            continue 
            
        if stripped_line.startswith('>'):
            if dna:
                if tags:
                    target.append([dna, tag])
                else:
                    target.append(dna)
                dna = ""
            tag = stripped_line.lstrip(">").strip()
        else:
            dna += stripped_line
            
    if dna:
        if tags:
            target.append([dna, tag])
        else:
            target.append(dna)
