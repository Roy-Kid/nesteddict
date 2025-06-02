import pytest
from nesteddict import ArrayDict

@pytest.fixture
def large_array_dict():
    """Fixture to create a deeply nested array-like dictionary."""
    data = {}
    for i in range(1000):
        data[f"key_{i}"] = {
            f"nested_key_{j}": [
                k for k in range(10)
            ] for j in range(100)
        }
    return data

def test_benchmark_init(benchmark, large_array_dict):
    """Benchmark the initialization of an ArrayDict with large data."""
    benchmark(ArrayDict, large_array_dict)

def test_benchmark_getitem(benchmark, large_array_dict):
    """Benchmark deeply nested key access in an ArrayDict."""
    array_dict = ArrayDict(large_array_dict)
    benchmark(lambda: array_dict["key_500"]["nested_key_50"][5])

def test_benchmark_setitem(benchmark, large_array_dict):
    """Benchmark deeply nested key updates in an ArrayDict."""
    array_dict = ArrayDict(large_array_dict)
    def update_deep_nested_key():
        array_dict["key_500"]["nested_key_50"][5] = 999
    benchmark(update_deep_nested_key)