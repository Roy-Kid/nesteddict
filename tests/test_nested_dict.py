import pytest

from nesteddict import NestedDict


class TestNestedDict:

    @pytest.fixture(scope="function", name="nd")
    def test_init(self):
        return NestedDict(
            {
                "a1": 1,
                "a2": {"b1": 2, "b2": {"c1": 3, "c2": {"d1": 4, "d2": 5}}},
                3: "a",
            }
        )

    def test_init_failed(self):
        with pytest.raises(TypeError):
            NestedDict(1)
            NestedDict([1, 2, 3])

    def test_traverse_failed(self, nd):

        assert nd._traverse(3)
        with pytest.raises(KeyError):
            nd._traverse((1, 2, 3))

    def test_delitem(self, nd):

        del nd["a1"]
        assert "a1" not in nd

        del nd[["a2", "b2", "c2", "d2"]]
        assert "d2" not in nd[["a2", "b2", "c2"]]

        with pytest.raises(KeyError):
            del nd["a2", "b2"]  # only list but tuple

    def test_eq(self):
        assert NestedDict({"a": 1}) == {"a": 1}
        assert NestedDict({"a": {"b": 2}}) != {"a": {"b": 1}}

    def test_bool(self, nd):
        assert nd
        assert not NestedDict()

    def test_getitem(self, nd):

        assert nd["a1"] == 1
        assert nd[["a2", "b1"]] == 2
        assert nd[["a2", "b2", "c1"]] == 3
        assert nd[["a2", "b2", "c2", "d1"]] == 4

    def test_setitem(self, nd):

        nd["a1"] = 10
        nd[["a2", "b1"]] = 20
        nd[["a2", "b2", "c1"]] = 30
        nd[["a2", "b2", "c2", "d1"]] = 40
        assert nd["a1"] == 10
        assert nd[["a2", "b1"]] == 20
        assert nd[["a2", "b2", "c1"]] == 30
        assert nd[["a2", "b2", "c2", "d1"]] == 40

        nd[["a3", "b1"]] = 50
        nd[["a3", "b2", "c1"]] = 60
        assert nd[["a3", "b1"]] == 50
        assert nd[["a3", "b2", "c1"]] == 60

        nd["tuple", "as", "key"] = 70
        assert nd[("tuple", "as", "key")] == 70

    def test_construct(self):

        nd = NestedDict(
            {
                "a": {"b": 1},
            }
        )
        assert nd[["a", "b"]] == 1
        nd[["a", "c"]] = 2
        assert nd[["a", "c"]] == 2

    def test_str(self):
        nd = NestedDict({"a": {"b": 1}})
        assert str(nd) == "<{'a': {'b': 1}}>"

    def test_repr(self):
        nd = NestedDict({"a": {"b": 1}})
        assert repr(nd) == "<{'a': {'b': 1}}>"

    def test_copy(self, nd):

        nd_copy = nd.copy()
        assert nd == nd_copy

    def test_flatten(self, nd):

        fd = nd.flatten()
        assert ("a1",) in fd
        assert ("a2", "b1") in fd

    def test_get(self, nd):

        assert nd.get("a1") == 1
        assert nd.get("a2.b1") == 2
        assert nd.get("a2.b2.c1") == 3
        assert nd.get("a2.b2.c2.d1") == 4

        assert nd.get("a3.b1") is None
        assert nd.get("a3.b2.c1") is None

    def test_set(self, nd):

        nd.set("a1", 10)
        nd.set("a2.b1", 20)
        nd.set("a2.b2.c1", 30)
        nd.set("a2.b2.c2.d1", 40)
        assert nd["a1"] == 10
        assert nd[["a2", "b1"]] == 20
        assert nd[["a2", "b2", "c1"]] == 30
        assert nd[["a2", "b2", "c2", "d1"]] == 40

        nd.set("a3.b1", 50)
        nd.set("a3.b2.c1", 60)
        assert nd[["a3", "b1"]] == 50
        assert nd[["a3", "b2", "c1"]] == 60

    def test_clear(self, nd):

        nd.clear()
        assert len(nd) == 0

    def test_keys(self, nd):

        keys = nd.keys()
        assert "a1" in keys
        assert "a2" in keys

    def test_values(self, nd):

        values = nd.values()
        assert 1 in values

    def test_iter(self, nd):

        for key in nd:
            assert key in nd.keys()

    def test_update_dict(self, nd):

        nd.update({"a1": 10, "a2": {"b1": 20, "b2": {"c1": 30, "c2": {"d1": 40}}}})
        assert nd["a1"] == 10
        assert nd[["a2", "b1"]] == 20
        assert nd[["a2", "b2", "c1"]] == 30
        assert nd[["a2", "b2", "c2", "d1"]] == 40

    def test_update_nested(self, nd):

        new_nd = NestedDict()
        new_nd.update(nd)

        assert new_nd["a1"] == 1
        assert new_nd[["a2", "b1"]] == 2
        assert new_nd[["a2", "b2", "c1"]] == 3
        assert new_nd[["a2", "b2", "c2", "d1"]] == 4


class TestBenchmark:

    @pytest.fixture(scope="function", name="nd")
    def test_init(self):
        return NestedDict(
            {"a1": 1, "a2": {"b1": 2, "b2": {"c1": 3, "c2": {"d1": 4, "d2": 5}}}}
        )

    def test_get(self, nd, benchmark):

        benchmark(nd.get, "a2.b2.c2.d2")

    def test_getitem(self, nd, benchmark):

        benchmark(nd.__getitem__, ["a2", "b2", "c2"])

    def test_set(self, nd, benchmark):

        benchmark(nd.set, "a2.b2.c2.d3", 1)

    def test_setitem(self, nd, benchmark):

        benchmark(nd.__setitem__, ["a2", "b2", "c2", "d3"], 1)


try:
    import tensordict
except ImportError:
    tensordict = None  # pragma: no cover


class TestNestedDictCompatibility:

    @pytest.fixture(scope="function", name="nd")
    def test_init(self):
        return NestedDict(
            {"a1": 1, "a2": {"b1": 2, "b2": {"c1": 3, "c2": {"d1": 4, "d2": 5}}}}
        )

    @pytest.mark.skipif(tensordict is None, reason="tensordict not installed")
    def test_tensordict(self, nd):
        td = tensordict.TensorDict(nd)
        assert td["a1"] == 1
        assert td["a2", "b1"] == 2
