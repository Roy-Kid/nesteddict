import pytest
from nesteddict import NestedDict


class TestNestedDict:

    @pytest.fixture(scope="function", name="nd")
    def test_init(self):
        return NestedDict(
            {"a1": 1, "a2": {"b1": 2, "b2": {"c1": 3, "c2": {"d1": 4, "d2": 5}}}}
        )

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

    def test_flatten(self, nd):

        fd = nd.flatten()
        assert "a1" in fd
        assert "a2.b1" in fd

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
            assert key in nd

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
