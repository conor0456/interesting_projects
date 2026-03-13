"""
https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/40671.pdf
"""

from cmath import inf
import hashlib
import pickle

class HyperLogLog:
    def __init__(self, number_of_registers=50):
        self.longest_prefix_registers = [0] * number_of_registers
        self.number_of_registers = number_of_registers
    
    def update(self, record):
        object_bytes = pickle.dumps(record)
        hashed_bytes = hashlib.sha256(object_bytes).digest()
        register = int.from_bytes(hashed_bytes, byteorder='big') % self.number_of_registers
        self.longest_prefix_registers[register] = max(self.longest_prefix_registers[register], self._count_leading_zeros(hashed_bytes))

    def cardinality(self):
        if sum(self.longest_prefix_registers) < 2:
            return 0
        return sum(map(lambda x: (2**x) / self.number_of_registers, self.longest_prefix_registers))

    def __add__(self, other):
        # TODO (Conor) Allow for merging of HLL instances
        pass
    
    def _count_leading_zeros(self, byte_array):
        leading_zeros = 0
        for byte in byte_array:
            i = 7
            while i > -1 and not ((byte >> i) & 1):
                leading_zeros += 1
                i -= 1
            if i != -1:
                return leading_zeros
        return leading_zeros
    
    """
    probability of seeing n 0s in a row is 2^-(n)
    """