import pytest
from nesteddict import NestDict

@pytest.fixture
def large_nested_dict():
    """Fixture to create a deeply nested dictionary."""
    data = {}
    for i in range(1000):
        data[f"key_{i}"] = {
            f"nested_key_{j}": {
                f"deep_key_{k}": k for k in range(10)
            } for j in range(100)
        }
    return data

def test_benchmark_init(benchmark, large_nested_dict):
    """Benchmark the initialization of a NestDict with large data."""
    benchmark(NestDict, large_nested_dict)

def test_benchmark_getitem(benchmark, large_nested_dict):
    """Benchmark deeply nested key access in a NestDict."""
    nest_dict = NestDict(large_nested_dict)
    benchmark(lambda: nest_dict["key_500"]["nested_key_50"]["deep_key_5"])

def test_benchmark_setitem(benchmark, large_nested_dict):
    """Benchmark deeply nested key updates in a NestDict."""
    nest_dict = NestDict(large_nested_dict)
    def update_deep_nested_key():
        nest_dict["key_500"]["nested_key_50"]["deep_key_5"] = 999
    benchmark(update_deep_nested_key)