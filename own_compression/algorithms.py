import time
def lz78_encode_ints(data):
    dictionary = {}
    indices = []
    values = []
    index = 1
    current = []

    for num in data:
        combined = current + [num]
        if tuple(combined) in dictionary:
            current = combined
        else:
            if current == []:
                indices.append(0)  # No prefix, just a fresh character
            else:
                indices.append(dictionary[tuple(current)])  # Existing prefix index
            values.append(num)  # Current character value
            dictionary[tuple(combined)] = index  # Add new combination to dictionary
            index += 1
            current = []  # Reset current prefix

    if current:
        indices.append(dictionary[tuple(current)])
        values.append(0)  # No new value after this (for an empty string case)
    return indices, values

def lz78_decode_ints(indices, values):
    dictionary = {0: []}  # Initial empty string mapped to 0
    result = []

    for idx, value in zip(indices, values):
        # Get the prefix from the dictionary, append the current value
        entry = dictionary[idx] + [value]
        result.extend(entry)  # Extend result with the current entry
        dictionary[len(dictionary)] = entry  # Add new entry to dictionary

    return result

class TrieNode:
    def __init__(self):
        self.children = {}
        self.index = 0

def lz78_encode_chars(text):
    start = time.time()
    root = TrieNode()
    indices = []
    characters = []
    current_node = root
    index = 1

    i = 0
    while i < len(text):
        ch = text[i]
        if ch in current_node.children:
            current_node = current_node.children[ch]
            i += 1
        else:
            indices.append(current_node.index)
            characters.append(ch)
            new_node = TrieNode()
            new_node.index = index
            current_node.children[ch] = new_node
            index += 1
            current_node = root
            i += 1

    # If there’s leftover text in a node
    if current_node != root:
        indices.append(current_node.index)
        characters.append('')

    end = time.time()
    print(f"Optimized LZ78: {end - start:.6f} seconds")
    return indices, characters

def lz78_decode_chars(indices, characters):
    dictionary = ['']
    result = ''

    for idx, ch in zip(indices, characters):
        entry = dictionary[idx] + ch
        result += entry
        dictionary.append(entry)

    return result

def delta_encode(data):
    if not data:
        return []
    deltas = [data[0]]
    for i in range(1, len(data)):
        deltas.append(data[i] - data[i - 1])
    return deltas

def delta_decode(deltas):
    if not deltas:
        return []
    data = [deltas[0]]
    for i in range(1, len(deltas)):
        data.append(data[-1] + deltas[i])
    return data
