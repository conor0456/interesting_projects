from hyper_log_log import HyperLogLog

def generate_bytes_with_leading_zeros(self, num_of_leading_zeros):
    assert num_of_leading_zeros <= 8, "Only 8 bits allowed at this time"
    bit_array = ['0'] * num_of_leading_zeros
    bit_array.extend(['1'] * (32 - num_of_leading_zeros))
    return int(''.join(bit_array), 2).to_bytes(4, byteorder='big')

def _convert_bit_array_to_int(self, bit_array):
    result_integer = 0
    for bit in bit_array:
        result_integer = (result_integer << 1) | bit
    return result_integer


def test_count_leading_zeros():
    hll = HyperLogLog()
    for i in range(8):
        assert hll._count_leading_zeros(hll.generate_bytes_with_leading_zeros(i)) == i

def test_cardinality_accuracy():
    randomizer = lambda x: f"{x}abc123"
    hll = HyperLogLog()
    for i in range(100_000_000):
        hll.update(randomizer(i))

        if i % 100_000 == 0:
            error = 100 * (i-hll.cardinality() ) / (hll.cardinality() + 1)
            print("Found cardinality of ", hll.cardinality(), " at count of ", i, " error: ", error, "registers: ", hll.longest_prefix_registers)
        


#test_count_leading_zeros()
test_cardinality_accuracy()




print("Tests complete!")