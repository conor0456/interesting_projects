from hyper_log_log import HyperLogLog

def _error_percent(expected, actual):
    return 100 * abs(expected - actual) / (expected + 1)

def test_cardinality_accuracy(iters = 10_000_000):
    randomizer = lambda x: f"{x}abc123"
    hll = HyperLogLog()
    for i in range(iters):
        hll.update(randomizer(i))

    error = _error_percent(iters, hll.cardinality())
    print("True Cardinality: ", iters, " Cardinality of H1: ", hll.cardinality(), " Error: ", error)
    assert error < 1, f"Error rate is over 1% for cardinality {iters}"
        
def test_merge_accuracy(iters = 1_000_000):
    hll1 = HyperLogLog()
    hll2 = HyperLogLog()
    for i in range(iters):
        hll1.update(f"a{i}")
        hll2.update(f"b{i}")
    merged = hll1 + hll2
    expected_merged_cardinality = 2 * iters
    error = _error_percent(expected_merged_cardinality, merged.cardinality())
    print("True Cardinality: ", iters, " Cardinality of H1: ", hll1.cardinality(), " H2: ", hll2.cardinality(), " Merged: ", merged.cardinality(), " Error: ", error)
    assert error < 1, f"Error rate is over 1% for cardinality {iters}"

def test_comparisons(iters = 1_000_000):
    hll1 = HyperLogLog()
    hll2 = HyperLogLog()
    hll1_duplicate = HyperLogLog()
    for i in range(iters):
        hll1.update(f"a{i}")
        hll1_duplicate.update(f"a{i}")
        if i % 10 == 0:
            hll2.update(f"b{i}")
    assert hll1 > hll2, "Greater than is incorrect"
    assert hll2 < hll1, "Less than is incorrect"
    assert hll1 == hll1_duplicate, "Equal is incorrect"

print("Starting tests!")
test_cardinality_accuracy()
test_merge_accuracy()
test_comparisons()
print("Tests complete!")