from typing import MutableMapping, Any, Iterator, Union
import numpy as np
import numpy.typing as npt
import io

NestedKey = str | list[str]  # type_check_only

from collections.abc import MutableMapping
import csv
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import h5py

# check if all arrays have same length
def _check_array_length(arrays: list[np.ndarray]) -> bool:
    """Check if all arrays have the same length.

    Args:
        arrays (list[np.ndarray]): List of numpy arrays to check.

    Returns:
        bool: True if all arrays have the same length, False otherwise.
    """
    lengths = [len(arr) for arr in arrays]
    return len(set(lengths)) < 2

class ArrayDict(MutableMapping):
    """A dictionary-like object that stores arrays."""

    _data: dict[str, np.ndarray]

    def __init__(self, source: dict = {}):
        source = {k: np.atleast_1d(v) for k, v in source.items()}
        super().__setattr__("_data", source)

    @classmethod
    def from_dicts(cls, source: list[dict]) -> "ArrayDict":
        """Create an ArrayDict from a list of dictionaries.

        Args:
            source (list[dict]): A list of dictionaries where each dictionary represents a row.

        Returns:
            ArrayDict: An ArrayDict where keys are the dictionary keys and values are arrays of the corresponding values.
        """

        keys = source[0].keys()
        data = {key: np.array([row[key] for row in source]) for key in keys}
        return cls(data)
    
    @classmethod
    def from_csv(
        cls,
        source: str | list[str] | io.StringIO,
        header: list[str] | None = None,
        seq: str = ",",
        **kwargs
    ) -> "ArrayDict":
        """Create an ArrayDict from a CSV file or CSV data with optional custom header and delimiter.

        Args:
            source (str|list[str]|io.StringIO): If str, path to the CSV file; if list of strings, CSV lines; if StringIO, CSV data.
            header (list[str]|None): Optional list of header fields.
            seq (str): Delimiter for CSV data.

        Returns:
            ArrayDict: An ArrayDict where keys are headers and values are arrays of the corresponding values.
        """
        if isinstance(source, str):
            with open(source, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, fieldnames=header, delimiter=seq, **kwargs)
                rows = [dict(row) for row in reader]
        elif isinstance(source, list):
            buffer = io.StringIO("\n".join(source))
            reader = csv.DictReader(buffer, fieldnames=header, delimiter=seq, **kwargs)
            rows = [dict(row) for row in reader]
        elif isinstance(source, io.StringIO):
            reader = csv.DictReader(source, fieldnames=header, delimiter=seq, **kwargs)
            rows = [dict(row) for row in reader]
        else:
            raise TypeError("Unsupported source type.")
        
        return cls.from_dicts(rows)


    def __getitem__(self, key: str | list[str] | slice) -> Union[np.ndarray, "ArrayDict"]:
        if isinstance(key, str):
            return self._data[key]
        elif isinstance(key, list):
            return ArrayDict({k: self._data[k] for k in key})
        elif isinstance(key, (slice, int, np.ndarray)):
            return ArrayDict({k: v[key] for k, v in self._data.items()})
        raise KeyError(f"Key {key} not support in ArrayDict")

    def __setitem__(
        self, key: str | list[str], value: Union[np.ndarray, "ArrayDict"]
    ) -> None:
        if isinstance(key, str) and isinstance(value, (np.ndarray, list)):
            self._data[key] = value
        elif isinstance(key, list) and isinstance(value, ArrayDict):
            for k in key:
                self._data[k] = value[k]
        elif isinstance(key, (slice, int)) and isinstance(value, ArrayDict):
            for k in self._data.keys():
                self._data[k][key] = value[k]
        else:
            raise KeyError(f"set type {type(value)} to '{key}' not support in ArrayDict")

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ArrayDict):
            value = other._data
        elif isinstance(other, dict):
            value = other
        else:
            return False
        return self._data.keys() == value.keys() and all([
            np.allclose(self[k], value[k]) for k in self._data.keys()
        ])

    @property
    def array_length(self) -> int:
        """Get the length of the arrays in the ArrayDict.

        Returns:
            int: The length of the arrays.
        """
        if not self._data:
            return 0
        return len(next(iter(self._data.values())))

    def iterrows(self):
        """Iterate over the rows of the array dictionary.

        Returns:
            Iterator[dict]: An iterator that yields dictionaries representing each row.
        """
        for i in range(self.array_length):
            yield self[i]

    def __repr__(self) -> str:
        return f"<ArrayDict: {' '.join(self._data.keys())}>"

    __str__ = __repr__

    def concat(self, other: "ArrayDict") -> "ArrayDict":
        """Concatenate two ArrayDict objects along the first axis.

        Args:
            other (ArrayDict): The other ArrayDict to concatenate with.

        Returns:
            ArrayDict: A new ArrayDict containing the concatenated data.
        """
        for key in self._data.keys():
            self[key] = np.concatenate((self[key], other[key]), axis=0)
        return self

    def to_hdf5(self, h5file: "h5py.File") -> "h5py.File":
        """Convert the ArrayDict to an HDF5 file.

        Returns:
            h5py.File: An HDF5 file containing the data from the ArrayDict.
        """

        for key, value in self._data.items():
            h5file.create_dataset(key, data=value)
        return h5file