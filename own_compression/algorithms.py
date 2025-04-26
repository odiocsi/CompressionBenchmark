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
                indices.append(0)
            else:
                indices.append(dictionary[tuple(current)])
            values.append(num)
            dictionary[tuple(combined)] = index
            index += 1
            current = []

    if current:
        indices.append(dictionary[tuple(current)])
        values.append(0)
    return indices, values

def lz78_decode_ints(indices, values):
    dictionary = {0: []}
    result = []

    for idx, value in zip(indices, values):
        entry = dictionary[idx] + [value]
        result.extend(entry)
        dictionary[len(dictionary)] = entry

    return result

import time
class TrieNode:
    def __init__(self, index = 0):
        self.children = {}
        self.index = index

def lz78_encode_chars(text):
    root = TrieNode()
    indices = []
    characters = []
    current_node = root
    index = 1

    for ch in text:
        if ch in current_node.children:
            current_node = current_node.children[ch]
            continue
        indices.append(current_node.index)
        characters.append(ch)
        current_node.children[ch] = TrieNode(index)
        index += 1
        current_node = root

    if current_node != root:
        indices.append(current_node.index)
        characters.append('')

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
