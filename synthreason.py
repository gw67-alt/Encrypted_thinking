import sys
import re

# Pronoun to Op Code Mapping (custom "op codes" as integers; extend as needed)
# Non-pronouns will default to 0x05 (XOR) for processing all words
PRONOUN_OP_CODES = {
    'I': 0x01,      # e.g., Op for addition
    'you': 0x02,    # e.g., Op for subtraction
    'he': 0x03,     # e.g., Op for multiplication
    'she': 0x04,    # e.g., Op for division (integer)
    'it': 0x05,     # e.g., Op for XOR
    'they': 0x06,   # e.g., Op for modulo
    # Add more pronouns or custom mappings here
}

# Default op code for non-pronouns
DEFAULT_OP_CODE = 0x05  # XOR, to ensure all words get algebraic processing

# Simple algebraic operations based on op codes
def apply_op_code(op_code, val1, val2):
    if op_code == 0x01: return val1 + val2
    elif op_code == 0x02: return val1 - val2
    elif op_code == 0x03: return val1 * val2
    elif op_code == 0x04: return val1 // val2 if val2 != 0 else 0
    elif op_code == 0x05: return val1 ^ val2  # XOR as core operation
    elif op_code == 0x06: return val1 % val2 if val2 != 0 else 0
    return val1  # Default: no-op

# Function to convert a word to a "hash" value defined by the word itself (sum of ord(c) % 2^16)
def word_defined_hash(word):
    hash_val = sum(ord(c) for c in word)
    return hash_val % (2**16)  # 16-bit value for simplicity

# Simple sentence tokenizer (split on ., !, ? without NLTK)
def simple_sent_tokenize(text):
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text.strip())

# Main processing function
def process_text(text):
    sentences = simple_sent_tokenize(text)
    results = []
    
    for sent_idx, sentence in enumerate(sentences):
        # Simple word tokenizer: split on spaces and punctuation
        words = re.findall(r'\b\w+\b', sentence.lower())  # Extract words only
        sent_result = {
            'sentence': sentence,
            'input_values': [],  # Positional inputs
            'output_values': [], # Retrieved outputs
            'algebraic_logic': []  # Expressed as strings
        }
        
        prev_hash = 0  # For chaining XOR retrieval
        for word_idx, word in enumerate(words):
            # Positional logic: Use word position as a base value
            pos_value = (sent_idx * len(words)) + word_idx  # Simple positional encoding
            
            # Determine op_code: Use mapping if pronoun, else default
            op_code = PRONOUN_OP_CODES.get(word, DEFAULT_OP_CODE)
            
            # Semantic retrieval: XOR current word-defined hash with previous for "retrieval"
            word_hash = word_defined_hash(word)
            retrieved_value = word_hash ^ prev_hash
            prev_hash = retrieved_value  # Chain for next
            
            # Apply op code algebraically with positional value
            output = apply_op_code(op_code, pos_value, retrieved_value)
            
            # Store input/output
            sent_result['input_values'].append(f"Pos:{pos_value}, Hash:{word_hash}")
            sent_result['output_values'].append(output)
            
            # Express as algebraic logic string
            logic_str = f"{word.upper()} (Op {hex(op_code)}) : {pos_value} ⊕ {word_hash} → {output}"
            sent_result['algebraic_logic'].append(logic_str)
        
        if sent_result['algebraic_logic']:  # Now always true if there are words
            results.append(sent_result)
    
    return results

# Input/Output Handling
def main():
    if len(sys.argv) > 1:
        # Read from file if provided as argument
        try:
            with open(sys.argv[1], 'r') as f:
                text = f.read()
        except FileNotFoundError:
            print("File not found. Using stdin instead.")
            text = sys.stdin.read()
    else:
        # Read from stdin
        print("Enter text (end with Ctrl+D or Ctrl+Z):")
        text = input("User:")
    
    if not text.strip():
        print("No input text provided.")
        return
    
    results = process_text(text)
    
    # Output results
    print("\nProcessed Results (Algebraic Logic with Input/Output):")
    for res in results:
        print(f"\nSentence: {res['sentence']}")
        print("Inputs:", res['input_values'])
        print("Outputs:", res['output_values'])
        print("Algebraic Logic:")
        for logic in res['algebraic_logic']:
            print(f"  {logic}")

if __name__ == "__main__":
    main()
