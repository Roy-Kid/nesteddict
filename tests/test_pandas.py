import pytest
from nesteddict import NestDict

pandas_found = True
try:
    import pandas as pd
except ImportError:
    pandas_found = False

@pytest.mark.skipif(
    not pandas_found, reason="pandas not installed"
)
class TestMixinPandas:

    @pytest.fixture(scope="class", name="pdict")
    def test_init(self):
        return NestDict(
            {
                "a1": 1,
                "a2": pd.DataFrame({
                    "b1": [1, 2, 3],
                    "b2": ["a", "b", "c"],
                }),
                3: "a",
            }
        )
    
    def test_getitem(self, pdict):
        assert pdict["a1"] == 1
        assert (pdict[["a2", "b1"]] == pd.Series([1, 2, 3])).all()
        assert (pdict[["a2", "b2"]] == pd.Series(["a", "b", "c"])).all()

    def test_setitem(self, pdict):
        pdict["a1"] = 10
        pdict[["a2", "b1"]] = pd.DataFrame({"b1": [10, 20, 30]})
        pdict[["a2", "b2"]] = pd.DataFrame({"b2": ["x", "y", "z"]})
        assert pdict["a1"] == 10
        assert pdict[["a2", "b1"]].iloc[0] == 10
        assert pdict[["a2", "b2"]].iloc[1] == "y"

    # def test_getattr(self, pdict):
    #     assert pdict.a1 == 10

    # def test_setattr(self, pdict):
    #     pdict.a1 = 20
    #     pdict.a2.b1.iloc[0, 0] = 20
    #     pdict.a2.b2.iloc[0, 0] = "y"
    #     assert pdict.a1 == 20