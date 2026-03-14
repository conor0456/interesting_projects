"""
https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/40671.pdf
"""

import hashlib
import pickle
from functools import total_ordering

@total_ordering
class HyperLogLog:
    HASH_RESULTING_BYTE_SIZE = 8 #64 bits
    def __init__(self, num_bits_for_register_mapping = 15):
        assert 0 < num_bits_for_register_mapping < 63, "Number of bits must be within range [1,62]"
        self.number_of_registers = 2**num_bits_for_register_mapping
        self.registers = [0] * self.number_of_registers
        self.num_bits_for_register_mapping = num_bits_for_register_mapping
        self.alpha = self._alpha()
    
    def update(self, record):
        object_bytes = pickle.dumps(record)
        hashed_bytes = hashlib.md5(object_bytes).digest()[:self.HASH_RESULTING_BYTE_SIZE]
        hashed_int = int.from_bytes(hashed_bytes, byteorder='big', signed=False)
        register, remainder = self._split_bits(hashed_int)
        self.registers[register] = max(self.registers[register], self._count_zeros(remainder))

    def merge(self, other):
        if not isinstance(other, HyperLogLog):
            return NotImplemented
        if not self.num_bits_for_register_mapping == other.num_bits_for_register_mapping: 
            raise ValueError("Merging HLLs requires registers of equal size!")
        
        for i in range(self.number_of_registers):
            self.registers[i] = max(self.registers[i], other.registers[i])
        return self
    
    def cardinality(self):        
        return int(self._raw_estimate() * self.alpha)

    def _split_bits(self, hashed_int):
        p = self.num_bits_for_register_mapping
        register = hashed_int >> (64 - p)
        remainder = hashed_int & ((1 << (64 - p)) - 1)

        return register, remainder
    
    def _count_zeros(self, remainder):
        q = 64 - self.num_bits_for_register_mapping 
        if remainder == 0:
            return q + 1
        return (q - remainder.bit_length()) + 1
    
    def _raw_estimate(self):
        Z = sum(2.0 ** (-register) for register in self.registers)
        return (self.number_of_registers ** 2) / Z
    
    def _alpha(self):
        """
        Alpha is an emperically determined constant set in relation to our number of registers
        """
        if self.number_of_registers == 16:
            return 0.673
        elif self.number_of_registers == 32:
            return 0.697
        elif self.number_of_registers == 64:
            return 0.709
        else:
            return 0.7213 / (1 + 1.079 / self.number_of_registers)

    def __add__(self, other):
        if not isinstance(other, HyperLogLog):
            return NotImplemented
        new_hll = HyperLogLog(self.num_bits_for_register_mapping)
        new_hll.registers = self.registers.copy()
        new_hll.merge(other)
        return new_hll
        
    def __lt__(self, other):
        if not isinstance(other, HyperLogLog):
            return NotImplemented
        return self.cardinality() < other.cardinality()

    def __eq__(self, other):
        if not isinstance(other, HyperLogLog):
            return NotImplemented
        return self.registers == other.registers