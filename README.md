![PyPI - License](https://img.shields.io/pypi/l/nesteddict)
![Codecov](https://img.shields.io/codecov/c/github/Roy-Kid/nesteddict)

# nesteddict

**NestedDict** is a subclass of Python's `dict` that fully implements all `dict` methods while adding support for automatic nesting. It simplifies working with hierarchical data by providing intuitive methods for accessing, updating, and managing multi-level structures, making it ideal for handling complex configurations and JSON-like data.

*quick start*:

``` python
from nesteddict import NestedDict

>>> d = {'path': {'to': {'key': 'val'}}}
>>> nd = NestedDict(d)
>>> nd[['path', 'to', 'key']]
'val'
>>> nd[['path', 'new', 'key']] = 'val'
>>> nd[['path', 'new']]
{'key', 'val'}
```
