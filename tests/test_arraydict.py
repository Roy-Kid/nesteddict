import pytest
import numpy as np
from nesteddict import ArrayDict

class TestNumpy:
    """
    Test class for Numpy operations.
    """

    @pytest.fixture(scope="function", name="ad")
    def test_init_(self):

        atoms =  ArrayDict({
            "id": np.array([1, 2, 3]),
            "type": np.array(["C1", "C2", "C3"]),
            "xyz": np.random.rand(3, 3),
        })
        # bonds = ArrayDict({
        #     "connectivity": np.array([[0, 1], [1, 2]]),
        #     "type": np.array(["bond1", "bond2"]),
        # })
        # angles = ArrayDict({
        #     "connectivity": np.array([[0, 1, 2]]),
        #     "type": np.array(["angle1"]),
        # })
        return atoms
    
    def test_getitem(self, ad):
        """
        Test the __getitem__ method of NestDict.
        """
        assert np.array_equal(ad["id"], np.array([1, 2, 3]))
        assert set(ad[["type", "xyz"]].keys()) == {"type", "xyz"}
        assert ad[1] == {
            "id": [2],
            "type": ["C2"],
            "xyz": ad["xyz"][1].reshape(1, -1),
        }
        assert ad[0:2] == {
            "id": np.array([1, 2]),
            "type": np.array(["C1", "C2"]),
            "xyz": ad["xyz"][0:2],
        }

    def test_setitem(self, ad):
        """
        Test the __setitem__ method of NestDict.
        """
        # Set a single item
        ad["id"] = np.array([4, 5, 6])
        assert np.array_equal(ad["id"], np.array([4, 5, 6]))

        # Set multiple items
        ad[["type", "xyz"]] = ArrayDict({
            "type": np.array(["C4", "C5", "C6"]),
            "xyz": np.random.rand(3, 3),
        })
        assert set(ad.keys()) == {"id", "type", "xyz"}
        assert np.array_equal(ad["type"], np.array(["C4", "C5", "C6"]))

        # Set a slice
        ad[0:2] = ArrayDict({
            "id": np.array([7, 8]),
            "type": np.array(["C7", "C8"]),
            "xyz": np.random.rand(2, 3),
        })
        assert np.array_equal(ad["id"][0:2], np.array([7, 8]))
        assert np.array_equal(ad["type"][0:2], np.array(["C7", "C8"]))
        assert np.array_equal(ad["xyz"][0:2], ad["xyz"][0:2])

    def test_getitem_invalid(self, ad):
        """
        Test the __setitem__ method of NestDict with invalid input.
        """
        with pytest.raises(KeyError):
            ad["invalid_key"]

        with pytest.raises(KeyError):
            ad[["invalid_key"]]

    def test_iterrows(self, ad):
        """
        Test the iterrows method of NestDict.
        """
        # Iterate over rows
        for i, row in enumerate(ad.iterrows()):
            assert isinstance(row, ArrayDict)
            assert "id" in row
            assert np.array_equal(row["xyz"], ad["xyz"][i].reshape(1, -1))