import random
'''Additional feature- user specifies nucleotide distrbution. 
The function takes input from the user for percentage distribution of bass and ensures that all inputs are integers 
between 0 and 100 and that the total is equal to 100. It retruns a dictionary contaning validated percentages'''
def get_nucleotide_distribution()->dict:
    while True:
        try:
            A = int(input("Enter percentage for A: "))
            C = int(input("Enter percentage for C: "))
            T = int(input("Enter percentage for T: "))
            G = int(input("Enter percentage for G: "))

            values = [A, C, T, G]
            if any(value < 0 or value > 100 for value in values):
                print("Error: each value must be between 0 and 100.")
                continue

            if sum(values) != 100:
                print("Error: percentages must sum to 100.")
                continue

            return {"A": A, "C": C, "T": T, "G": G}
        except ValueError:
            print("Error: percentages must be integers.")

'''This function generates the nucleotide sequence given the length and desired distribution. It returns the generated sequence as a string'''
def generate_sequence_custom_distribution (length: int, distribution: dict) -> str:
    nucleotides=['A','C','T','G']
    weights = [distribution[n] for n in nucleotides]
    sequence = "".join(random.choices(nucleotides, weights=weights, k=length))#generate the sequence using weighted 'random' selection.
    return sequence

#Additional feature: translation
codon_table = {
    "TTT": "Phe", "TTC": "Phe", "TTA": "Leu", "TTG": "Leu",
    "TCT": "Ser", "TCC": "Ser", "TCA": "Ser", "TCG": "Ser",
    "TAT": "Tyr", "TAC": "Tyr", "TAA": "Stop", "TAG": "Stop",
    "TGT": "Cys", "TGC": "Cys", "TGA": "Stop", "TGG": "Trp",

    "CTT": "Leu", "CTC": "Leu", "CTA": "Leu", "CTG": "Leu",
    "CCT": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "CAT": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln",
    "CGT": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",

    "ATT": "Ile", "ATC": "Ile", "ATA": "Ile", "ATG": "Met",
    "ACT": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    "AAT": "Asn", "AAC": "Asn", "AAA": "Lys", "AAG": "Lys",
    "AGT": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",

    "GTT": "Val", "GTC": "Val", "GTA": "Val", "GTG": "Val",
    "GCT": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
    "GAT": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
    "GGT": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly"
}
'''This function translated a DNA sequence into a protein sequence using the codon table above. 
It takes the sequence as an argument and returns the amino acid sequence as a string'''
def translate_sequence(sequence: str)-> str:
    protein=[]
    for i in range(0, len(sequence) - 2, 3):#Iterate over the sequence in steps of 3. We stop at len-2 to avoid incomplete codon at the end of the sequence.
        codon = sequence[i:i + 3]
        amino_acid = codon_table.get(codon, "?")#Unnown codons are marked as ?
        if amino_acid == "Stop":
            break

        protein.append(amino_acid)

    return " ".join(protein)

'''Additional feature: searching for motifs
This function finds all occurences of a certain sequence specified by the user. It returns a list of positions of the motifs in the sequence'''
def find_motif(sequence: str, motif: str) -> list:
    #Normalize input to make sure it matches the sequence formatting
    sequence = sequence.upper()
    motif = motif.upper()
    positions = []
    for i in range(len(sequence) - len(motif) + 1):
        if sequence[i:i + len(motif)] == motif:
            positions.append(i + 1)#Convert to 1- based indexing
    return positions

'''Additional feature: in silico transcription. All T nucleotides in the sequence are replaced with U.'''
def transcribe_sequence(sequence: str) -> str:
    return sequence.upper().replace("T", "U")

'''The function generates a random DNA sequence of a given length. It returns the sequence as a string'''
def generate_sequence (length: int) -> str:
    nucleotides=['A','C','T','G']
    sequence=''
    for _ in range(length):
        nucleotide=random.choice(nucleotides)#Nucleotide is randomly selected from the list with equal probability
        sequence+=nucleotide#Nucleotide is appended to the sequence
    return sequence

'''This function calculates nuclotide statistics for a given DNA sequence. 
It counts the occurances of every nucleotide, converts them into percentages and calculates GC content. 
GC represents the percentage of nucleotides in the sequence that are either Guanine or Cytosine. 
The function returns a dictionary containing percentages of each nucleotide in the sequence'''
def calculate_stats (sequence: str) -> dict :
    stats_raw={"A":sequence.count('A'),"C":sequence.count('C'),"T":sequence.count('T'),"G":sequence.count('G')}#Count occurances in the sequence
    length = len(sequence)
    stats={}
    for nucleotide in stats_raw:
        stats[nucleotide]=round((stats_raw[nucleotide]/length)*100,2)#Calculate percentage
    gc_stats = stats_raw['G'] + stats_raw['C']
    stats['GC']=round((gc_stats/length)*100,2)#Calculate percentage of GC
    return stats

'''This function inserts the given name at a random position in the provided sequence and returns the sequence with name inserted'''
def insert_name (sequence: str, name: str) -> str:
    sequence=sequence.upper()
    name=name.lower()#Name is in lowercase as specified by the assignemnt
    pos = random.randint(0, len(sequence))#Randomly choose a place to insert the name
    new_sequence = sequence[:pos]+name+sequence[pos:]#Use string slicing to create new string with sequence and name inserted
    return new_sequence

'''Thos function formats a sequence into FASTA and saves it to a file. It returns the sequence in FASTA format'''
def format_fasta ( seq_id : str , description : str ,
                 sequence: str, line_width : int = 80) -> str:
    if description:
        header = f">{seq_id} {description}"#If description was provided, include it
    else:
        header = f">{seq_id}"
    lines = [sequence[i:i+line_width] for i in range(0, len(sequence), line_width)]#Split the sequence into lines of length specified as the argument
    fasta_str = header + "\n" + "\n".join(lines)#Combine header and sequence
    filename = f"{seq_id}.fasta"
    with open(filename, "w") as f:
        f.write(fasta_str)
    return fasta_str

'''This function is used to validate whether the length for the sequence that is specified by the user is an integer and in the correct range. 
If it is not, the function prints an error and prompts the user to try again'''
def validate_positive_int (prompt: str,
                          min_val : int = 1,
                          max_val : int = 100_000) -> int:
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
    #Ask user for desired length of sequence
    length = validate_positive_int("Enter sequence length: ")
    #Ask user whether they would like to provide custom distributions or use random distributions
    while True:
        custom = input("Would you like to provide distributions? (y/n): ").lower()
        if custom == "y":
            distribution = get_nucleotide_distribution()
            sequence = generate_sequence_custom_distribution(length, distribution)
            break
        elif custom == "n":
            sequence = generate_sequence(length)
            break
        else:
            print("Please enter 'y' or 'n'.")
    #Ask user to enter sequence ID and validate whether it contains whitespaces.
    while True:
        seq_id=input("Enter sequence ID: ")
        if any(c.isspace() for c in seq_id):
            print("Error: Sequence ID cannot contain whitespace.")
        else:
            break
    #Ask user for description of the sequence (can be empty)
    description = input("Enter a description of the sequence: ")
    #Ask user for name to be inserted into the sequence
    name = input("Enter your name: ")
    #Insert the name and save the sequence
    sequence_with_name = insert_name(sequence, name)
    format_fasta(seq_id, description, sequence_with_name)
    print(f"\nSequence saved to file: {seq_id}.fasta")
    #Calculate statistics (for the original sequence without name inserted)
    print(calculate_stats(sequence))
    #Translate sequence
    print(f"\nTranslated sequence:")
    print(translate_sequence(sequence))
    #Search motif in the sequence
    motif = input("\nEnter motif to search: ")
    positions = find_motif(sequence, motif)
    if positions:
        print(f"Motif found at positions: {' '.join(map(str, positions))}")
    else:
        print("Motif not found.")
    #Transcribe sequence and save to another FASTA file
    rna=transcribe_sequence(sequence)
    rna_id=seq_id+'_mRNA'
    format_fasta(rna_id, description, rna)
    print(f"\nmRNA sequence saved to file: {seq_id}_mRNA.fasta")

if __name__ == "__main__":
    main ()
