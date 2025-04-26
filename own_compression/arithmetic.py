from functools import lru_cache
import numpy as np
import gmpy2
from gmpy2 import mpfr, get_context

class ArithmeticEncoder:
    def __init__(self):
        self.__chunk_size = 1000
        gmpy2.get_context().precision = 5000

    def __calculate_probabilities(self, data):
        arr = np.array(list(data))
        unique, counts = np.unique(arr, return_counts=True)
        total = len(arr)
        return dict(zip(unique, counts / total))


    @lru_cache(maxsize=2048)
    def get_symbol_ranges(self, prob_tuple):
        cumulative = mpfr(0)
        ranges = {}

        for symbol, p in prob_tuple:
            p_mpf = mpfr(p)
            symbol_low = cumulative
            symbol_high = cumulative + p_mpf
            ranges[symbol] = (symbol_low, symbol_high)
            cumulative = symbol_high

        return ranges

    def __arithmetic_encoder(self, data, prob):
        low = mpfr(0)
        high = mpfr(1)

        sorted_prob = tuple(sorted(prob.items()))
        base_ranges = self.get_symbol_ranges(sorted_prob)
        for char in data:
            range_width = high - low

            symbol_low, symbol_high = base_ranges[char]

            low = low + range_width * symbol_low
            high = low + range_width * (symbol_high - symbol_low)

        return (low + high) / 2


    @lru_cache(maxsize=2048)
    def get_decoder_ranges(self, prob_tuple, range_width, low):
        cumulative = low
        ranges = {}

        for symbol, p in prob_tuple:
            p_mpf = mpfr(p)
            symbol_low = cumulative
            symbol_high = cumulative + p_mpf * range_width
            ranges[symbol] = (symbol_low, symbol_high)
            cumulative = symbol_high

        return ranges

    def __arithmetic_decoder(self, num, prob, length):
        num = mpfr(num)
        low = mpfr(0)
        high = mpfr(1)
        output = ""

        sorted_prob = tuple(sorted(prob.items()))

        for _ in range(length):
            range_width = high - low

            ranges = self.get_decoder_ranges(sorted_prob, range_width, low)

            for symbol, (symbol_low, symbol_high) in ranges.items():
                if symbol_low <= num < symbol_high:
                    output += str(symbol)
                    low, high = symbol_low, symbol_high
                    break

        return output
    def __split_data(self, data):
        return [data[i:i+self.__chunk_size] for i in range(0, len(data), self.__chunk_size)]

    def encode(self, data):
        chunks = self.__split_data(data)

        encoded_chunks = []
        prob_tables = []
        chunk_sizes = []
        for chunk in chunks:
            prob = self.__calculate_probabilities(chunk)
            encoded_chunk = self.__arithmetic_encoder(chunk, prob)
            chunk_size = len(chunk)


            encoded_chunks.append(encoded_chunk)
            prob_tables.append(prob)
            chunk_sizes.append(chunk_size)


        encoded_data = encoded_chunks

        return encoded_data, prob_tables, chunk_sizes

    def decode(self, data, prob_tables, chunk_sizes):
        decoded_chunks = []
        for n in range(len(data)):
            decoded_chunk = self.__arithmetic_decoder(data[n], prob_tables[n], chunk_sizes[n])
            decoded_chunks.append(decoded_chunk)

        decoded_data = ''.join(decoded_chunks)

        return decoded_data
