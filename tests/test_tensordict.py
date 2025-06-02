import pytest

tensordict_found = True
try:
    import tensordict
except ImportError:
    tensordict_found = False  # pragma: no cover

from nesteddict import NestDict

@pytest.mark.skipif(
    not tensordict_found, reason="tensordict not installed"
)
class TestNestDictCompatibility:

    @pytest.fixture(scope="function", name="nd")
    def test_init(self):
        return NestDict(
            {"a1": 1, "a2": {"b1": 2, "b2": {"c1": 3, "c2": {"d1": 4, "d2": 5}}}}
        )

    @pytest.mark.skipif(tensordict_found, reason="tensordict not installed")
    def test_tensordict(self, nd):
        td = tensordict.TensorDict(nd)
        assert td["a1"] == 1
        assert td["a2", "b1"] == 2
