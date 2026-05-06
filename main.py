import random

def generate_sequence (length: int) -> str:
    """Returns a random DNA sequence of the specified length."""
    nucleotides=['A','C','T','G']
    sequence=''
    for _ in range(length):
        nucleotide=random.choice(nucleotides)
        sequence+=nucleotide
    return sequence

def calculate_stats (sequence: str) -> dict :
    """Returns a dictionary of sequence statistics.
Keys: "A", "C", "G", "T" ( float values , %),
           "GC" ( float value , %)."""
    stats_raw={"A":sequence.count('A'),"C":sequence.count('C'),"T":sequence.count('T'),"G":sequence.count('G')}
    length = len(sequence)
    stats={}
    for nucleotide in stats_raw:
        stats[nucleotide]=round((stats_raw[nucleotide]/length)*100,2)
    gc_stats = stats_raw['G'] + stats_raw['C']
    stats['GC']=round((gc_stats/length)*100,2)
    return stats

def insert_name (sequence: str, name: str) -> str:
    """Inserts a name at a random position in the sequence.
Name written in lowercase letters."""
    sequence=sequence.upper()
    name=name.lower()
    pos = random.randint(0, len(sequence))
    new_sequence = sequence[:pos]+name+sequence[pos:]
    return new_sequence

def format_fasta ( seq_id : str , description : str ,
                 sequence: str, line_width : int = 80) -> str:
    """Returns a formatted FASTA record as a string."""
    if description:
        header = f">{seq_id} {description}"
    else:
        header = f">{seq_id}"
    lines = [sequence[i:i+line_width] for i in range(0, len(sequence), line_width)]
    fasta_str = header + "\n" + "\n".join(lines)
    filename = f"{seq_id}.fasta"
    with open(filename, "w") as f:
        f.write(fasta_str)
    return fasta_str

def validate_positive_int (prompt: str,
                          min_val : int = 1,
                          max_val : int = 100_000) -> int:
    """Gets an integer from the user in a range.
In case of an error, repeats the question."""
    while True:
        value = input(prompt)
        try:
            num = int(value)
            if min_val <= num <= max_val:
                return num
            else:
                print("Error: value must be an integer in the range [1, 100000].")
        except ValueError:
            print("Error: value must be an integer in the range [1, 100000].")

def main ():
    length = validate_positive_int("Enter sequence length: ")
    sequence = generate_sequence(length)
    while True:
        seq_id=input("Enter sequence ID: ")
        if any(c.isspace() for c in seq_id):
            print("Error: Sequence ID cannot contain whitespace.")
        else:
            break
    description = input("Enter a description of the sequence: ")
    name = input("Enter your name: ")
    sequence_with_name = insert_name(sequence, name)
    format_fasta(seq_id, description, sequence_with_name)
    print(f"\nSequence saved to file: {seq_id}.fasta")
    print(calculate_stats(sequence))

if __name__ == "__main__":
    main ()

