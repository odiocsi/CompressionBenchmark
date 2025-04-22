import own_compression.arithmetic as ar
import own_compression.algorithms as alg
from mpmath import mpf
import numpy as np
from decimal import Decimal, getcontext

class Compressor:
    def __init__(self):
        self.__arCompressor = ar.ArithmeticEncoder()

    def compress(self, data):
        indicies, encoded_chars = alg.lz78_encode_chars(data)

        encoded_indicies = alg.delta_encode(indicies)

        indi1, indi2 = alg.lz78_encode_ints(encoded_indicies)

        encoded_data, prob_tables, chunk_size = self.__arCompressor.encode(encoded_chars)

        return [indi1, indi2, encoded_data, prob_tables, chunk_size]

    def decompress(self, data):
        data = eval(data)
        decoded = self.__arCompressor.decode(data[2], data[3], data[4])
        encoded_indicies = alg.lz78_decode_ints(data[0], data[1])

        decoded = list(decoded)
        decoded_indicies = alg.delta_decode(encoded_indicies)
        decoded.append('')


        decoded_text = alg.lz78_decode_chars(decoded_indicies, decoded).replace("\\n", "\n")

        return decoded_text


