import pytest
import numpy as np
from nesteddict import ArrayDict
import io
try:
    import h5py
except ImportError:
    h5py = None

class TestNumpy:
    """
    Test class for Numpy operations.
    """

    @pytest.fixture(scope="function", name="ad")
    def test_init_(self):

        atoms =  ArrayDict({
            "scalar": np.array([1, 2, 3]),
            "vectorial": np.random.rand(3, 3),
            "tensorial": np.random.rand(3, 3, 3),
        })
        return atoms
    
    def test_getitem(self, ad):
        """
        Test the __getitem__ method of NestDict.
        """
        assert np.array_equal(ad["scalar"], np.array([1, 2, 3]))
        assert set(ad[["scalar", "vectorial"]].keys()) == {"scalar", "vectorial"}
        assert ad[1] == {
            "scalar": [2],
            "vectorial": ad["vectorial"][1],
            "tensorial": ad["tensorial"][1],
        }
        assert ad[0:2] == {
            "scalar": np.array([1, 2]),
            "vectorial": ad["vectorial"][0:2],
            "tensorial": ad["tensorial"][0:2],
        }

    def test_setitem(self, ad):
        """
        Test the __setitem__ method of NestDict.
        """
        # Set a single item
        ad["scalar"] = np.array([4, 5, 6])
        assert np.array_equal(ad["scalar"], np.array([4, 5, 6]))

        # Set multiple items
        ad[["scalar", "vectorial"]] = ArrayDict({
            "scalar": np.array([4, 5, 6]),
            "vectorial": np.random.rand(3, 3),
            "tensorial": np.random.rand(3, 3, 3),
        })
        assert set(ad.keys()) == {"scalar", "vectorial", "tensorial"}
        assert np.array_equal(ad["scalar"], np.array([4, 5, 6]))

        # Set a slice
        ad[0:2] = ArrayDict({
            "scalar": np.array([7, 8]),
            "vectorial": np.random.rand(2, 3),
            "tensorial": np.random.rand(2, 3, 3),
        })
        assert np.array_equal(ad["scalar"][0:2], np.array([7, 8]))
        assert np.array_equal(ad["vectorial"][0:2], ad["vectorial"][0:2])

        with pytest.raises(ValueError):
            ad[0: 2] = ArrayDict({
                "scalar": np.array([4, 5, 6]),
                "vectorial": np.random.rand(3, 3),
                "tensorial": np.random.rand(3, 3, 3),
            })

        with pytest.raises(KeyError):
            ad[0: 2] = ArrayDict({
                "scalar": np.array([4, 5]),
                "tensorial": np.random.rand(3, 3),
            })
        

    def test_getitem_invalscalar(self, ad):
        """
        Test the __setitem__ method of NestDict with invalscalar input.
        """
        with pytest.raises(KeyError):
            ad["invalscalar_key"]

        with pytest.raises(KeyError):
            ad[["invalscalar_key"]]

    def test_iterrows(self, ad):
        """
        Test the iterrows method of NestDict.
        """
        # Iterate over rows
        for i, row in enumerate(ad.iterrows()):
            assert isinstance(row, ArrayDict)
            assert "scalar" in row
            assert row["vectorial"].shape == ad["vectorial"][i].shape

    def test_from_dicts(self):
        """
        Test the from_dicts method of ArrayDict.
        """
        dicts = [
            {"scalar": 1, "vectorial": np.random.rand(3)},
            {"scalar": 2, "vectorial": np.random.rand(3)},
            {"scalar": 3, "vectorial": np.random.rand(3)},
        ]
        ad = ArrayDict.from_dicts(dicts)
        assert len(ad) == 2
        assert set(ad.keys()) == {"scalar", "vectorial"}

    def test_to_hdf5(self, ad, tmp_path):
        """
        Test the to_hdf5 method of ArrayDict.
        """
        h5py_path = tmp_path / "test.h5"
        ad.to_hdf5(h5py_path)
        
        import h5py
        with h5py.File(h5py_path, "r") as f:
            assert "scalar" in f
            assert "vectorial" in f
            assert np.array_equal(f["scalar"][:], ad["scalar"])
            assert np.array_equal(f["vectorial"][:], ad["vectorial"])

    def test_to_hdf5_in_bytes(self, ad):
        """
        Test the to_hdf5_bytes method of ArrayDict.
        """
        h5py_bytes = ad.to_hdf5(path=None)
        
        import h5py
        with h5py.File(h5py_bytes, "r") as f:
            assert "scalar" in f
            assert "vectorial" in f
            assert np.array_equal(f["scalar"][:], ad["scalar"])
            assert np.array_equal(f["vectorial"][:], ad["vectorial"])
