import heapq

# --- 1. HuffmanNode Class ---
class HuffmanNode:
    """Represents a node in the Huffman Coding Tree."""
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    # Comparison method for the Priority Queue (Min Heap)
    # Compares nodes based on their frequency (required by heapq)
    def __lt__(self, other):
        return self.freq < other.freq

# --- 2. Build Tree and Generate Codes ---

def build_huffman_tree(text):
    """Calculates frequencies and builds the Huffman Tree."""
    
    # Step 2a: Calculate Frequencies
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1

    # Step 2b: Create Priority Queue (Min Heap)
    # Start with a list of all leaf nodes (character and frequency)
    priority_queue = []
    for char, freq in frequencies.items():
        # Using HuffmanNode class to create leaf nodes
        heapq.heappush(priority_queue, HuffmanNode(char=char, freq=freq))

    # Step 2c: Build the Tree
    # Repeat until only one node (the root) remains
    while len(priority_queue) > 1:
        # 1. Extract the two nodes with the lowest frequency
        left_node = heapq.heappop(priority_queue)
        right_node = heapq.heappop(priority_queue)

        # 2. Create a new internal node
        # Internal nodes have no character (char=None)
        new_freq = left_node.freq + right_node.freq
        internal_node = HuffmanNode(freq=new_freq, left=left_node, right=right_node)

        # 3. Add the new internal node back to the queue
        heapq.heappush(priority_queue, internal_node)

    # The last node remaining is the root of the Huffman Tree
    return priority_queue[0]

def generate_huffman_codes(root):
    """Traverses the tree to generate the binary codes for each character."""
    codes = {}
    # Helper function to traverse the tree recursively
    def traverse(node, current_code):
        if node is None:
            return

        # If it's a Leaf Node (it has a character)
        if node.char is not None:
            codes[node.char] = current_code if current_code else "0"  # Handle single character case
            return

        # Go Left (add '0')
        traverse(node.left, current_code + "0")
        
        # Go Right (add '1')
        traverse(node.right, current_code + "1")

    # Start traversal from the root with an empty initial code
    traverse(root, "")
    return codes

# --- 3. Encoding and Decoding ---

def encode(text, huffman_codes):
    """Encodes the input text using the generated Huffman codes."""
    encoded_text = ""
    for char in text:
        encoded_text += huffman_codes[char]
    return encoded_text

def decode(encoded_text, root):
    """Decodes the binary string back to the original text."""
    decoded_text = ""
    current_node = root

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else: # bit == '1'
            current_node = current_node.right
        
        # Check if we reached a Leaf Node (meaning we found a character)
        if current_node.char is not None:
            decoded_text += current_node.char
            # Reset back to the root for the next character
            current_node = root
            
    return decoded_text

# --- 4. Main Execution Block (Kaisa Run hoga check karne ke liye) ---

if __name__ == "__main__":
    # Input Data
    input_string = "huffman coding is a data compression algorithm"
    
    print(f"Original Text: '{input_string}'")
    print(f"Original Size (bits, roughly): {len(input_string) * 8}") # Assuming 8 bits per character (ASCII)

    # --- Step 1 & 2: Build Tree and Codes ---
    print("\n--- Building Tree and Codes ---")
    
    # Build the Huffman Tree (Returns the root node)
    huffman_tree_root = build_huffman_tree(input_string)
    
    # Generate the Huffman Codes (e.g., {'a': '01', 'b': '101', ...})
    codes = generate_huffman_codes(huffman_tree_root)
    
    print("Generated Huffman Codes:")
    for char, code in sorted(codes.items()):
        print(f"  '{char}': {code}")
        
    # --- Step 3: Encoding and Decoding ---
    print("\n--- Encoding and Decoding ---")
    
    # Encode the text
    encoded_data = encode(input_string, codes)
    print(f"Encoded Binary: {encoded_data}")
    print(f"Encoded Size (bits): {len(encoded_data)}")
    
    # Decode the text
    decoded_data = decode(encoded_data, huffman_tree_root)
    print(f"Decoded Text: '{decoded_data}'")
    
    # Verification
    if input_string == decoded_data:
        print("\n✅ Verification Successful: Decoded text matches the original text.")