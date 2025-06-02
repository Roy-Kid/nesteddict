# NestedDict: A Python Library for Heterogeneous Data
![PyPI - License](https://img.shields.io/pypi/l/NestDict)
![Codecov](https://img.shields.io/codecov/c/github/Roy-Kid/NestDict)

NestedDict is a Python library that extends the built-in `dict` to provide seamless support for nested data structures. It allows developers to effortlessly work with deeply nested dictionaries, enabling intuitive access, updates, and management of hierarchical data. Whether you're dealing with complex configurations, JSON-like data, or multi-level mappings, NestedDict simplifies your workflow with its automatic nesting capabilities and familiar dictionary interface.

---

## Features

- **NestDict**: A dictionary-like object for managing deeply nested data structures.
- **ArrayDict**: A dictionary-like object optimized for array-like data with consistent lengths.
- Intuitive access and updates for nested keys.
- Support for flattening and concatenating nested data structures.

---

## Installation

Install the library using pip:

```bash
pip install nesteddict
```

---

## Usage

### NestDict

`NestDict` is designed for managing deeply nested dictionaries with intuitive access and update capabilities.

#### Initialization

```python
from nesteddict import NestDict

# Initialize an empty NestDict
nd = NestDict()

# Initialize with a nested dictionary
nd = NestDict({'a': {'b': {'c': 1}}})
```

#### Accessing Nested Keys

```python
# Access using a list of keys
print(nd[['a', 'b', 'c']])  # Output: 1

# Access using a dot-separated string
print(nd.get('a.b.c'))  # Output: 1
```

#### Updating Nested Keys

```python
# Update using a list of keys
nd[['a', 'b', 'c']] = 2
print(nd[['a', 'b', 'c']])  # Output: 2

# Update using a dot-separated string
nd.set('a.b.c', 3)
print(nd.get('a.b.c'))  # Output: 3
```

#### Flattening Nested Structures

```python
# Flatten the nested dictionary
flat_dict = nd.flatten()
print(flat_dict)  # Output: {('a', 'b', 'c'): 1}
```

#### Concatenating NestedDicts

```python
nd1 = NestDict({'a': {'b': 1}})
nd2 = NestDict({'a': {'c': 2}})
nd1.concat(nd2)
print(nd1)  # Output: {'a': {'b': 1, 'c': 2}}
```

---

### ArrayDict

`ArrayDict` is optimized for managing array-like data with consistent lengths.

#### Initialization

```python
from nesteddict import ArrayDict
import numpy as np

# Initialize with array-like data
ad = ArrayDict({
    'a': [1, 2, 3],
    'b': np.array([4, 5, 6])
})
```

#### Accessing Data

```python
# Access a single key
print(ad['a'])  # Output: [1 2 3]

# Access multiple keys
print(ad[['a', 'b']])  # Output: <ArrayDict: a b>

# Access rows using slicing
print(ad[1])  # Output: <ArrayDict: a b>
```

#### Updating Data

```python
# Update a single key
ad['a'] = [7, 8, 9]

# Update rows using slicing
ad[1] = ArrayDict({'a': [10], 'b': [11]})
```

#### Iterating Over Rows

```python
# Iterate over rows
for row in ad.iterrows():
    print(row)
```

#### Concatenating ArrayDicts

```python
ad1 = ArrayDict({'a': [1, 2], 'b': [3, 4]})
ad2 = ArrayDict({'a': [5, 6], 'b': [7, 8]})
ad1.concat(ad2)
print(ad1)  # Output: <ArrayDict: a b>
```

---

## Benchmarks

The library includes benchmarks for both `NestDict` and `ArrayDict` to evaluate performance with large datasets. Run the benchmarks using `pytest`:

```bash
pytest --benchmark-only
```

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.