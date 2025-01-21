import operator
from functools import reduce
from typing import MutableMapping, Any, Iterator

NestedKey = str | list[str]  # type_check_only

#User Exceptions
class NestedKeyError(Exception): pass #currently only used to track NestedKey errors durning _construct_path

class NestedDictBase(MutableMapping):
    ...

class NestedDict(NestedDictBase):
    
    def __init__(self, source: dict|None = None):
        """Initializes a NestedDict with or without a source dictionary.

        Args:
            source (dict | None, optional): Source dictionary. Defaults to None.

        Raises:
            TypeError: source must be a dict

        Examples:
        
        >>> nd = NestedDict()
        >>> len(nd)
        0
        >>> NestedDict({"a": 1, "b": 2}).keys()
        dict_keys(['a', 'b'])
        >>> nd = NestedDict({'a': {'b': {'c': 1}}})
        >>> nd[['a', 'b', 'c']]
        1
        >>> nd.get('a.b.c')
        1
        """
        if source and not isinstance(source, dict):
            raise TypeError(f"source must be a dict, not {type(source)}")
        
        self._data = source or {}
        
    @staticmethod
    def _construct(data, nested_key: NestedKey, factory: type = dict):
        """ _construct_path is a recursive function that constructs a nested path in a dictionary.

        Args:
            data (dict): The dictionary to construct the path in.
            nested_key (NestedKey): The nested path to construct.

        Returns:
            dict: The constructed dictionary.
        """
        if nested_key:
            key = nested_key[0]
            if key not in data:
                data[key] = factory()
            return NestedDict._construct(data[key], nested_key[1:], factory)
        
    def _traverse(self, nested_key: NestedKey, construct: bool = False) -> Any:
        """Traverses a nested path in a dictionary.

        Args:
            nested_key (NestedKey): The nested path to traverse.
            construct (bool, optional): if create new container . Defaults to False.

        Raises:
            NestedKeyError: nested_key must be a str or list, not {type(nested_key)}

        Returns:
            Any: The value at the end of the nested path.
        """
        if construct:
            self._construct(self._data, nested_key)
        
        if isinstance(nested_key, str):
            return self._data[nested_key]
        elif isinstance(nested_key, list):
            return reduce(operator.getitem, nested_key, self._data)
        else:
            raise NestedKeyError(f"nested_key must be a str or list, not {type(nested_key)}")
        
    def __bool__(self) -> bool:
        return bool(self._data)
    
    def __eq__(self, other: Any) -> bool:
        return self._data == other
    
    def flatten(self, sep: str = ".") -> dict:
        """ get a python dict with a flat structure. The key is the nested key joined by the separator.

        Args:
            separator (str, optional): separator of nested key. Defaults to ".".

        Returns:
            dict: a python dict with a flat structure.

        Examples:
            >>> NestedDict({'a': {'b': {'c': 1}}}).flatten()
            {'a.b.c': 1}
            >>> NestedDict({'a': {'b': {'c': 1}}}).flatten(sep="/")
            {'a/b/c': 1}
        """
        def _flatten(data, parent_key = "", sep = "."):
            items = []
            for k, v in data.items():
                new_key = parent_key + sep + k if parent_key else k
                if isinstance(v, MutableMapping):
                    items.extend(_flatten(v, new_key, sep))
                else:
                    items.append((new_key, v))
            return items
        
        return dict(_flatten(self._data, "", sep))
    
    @classmethod
    def _nestize(cls, ):
        ...

    def __getitem__(self, nested_key: NestedKey) -> Any:
        item = self._traverse(nested_key)
        return item
    
    def __delitem__(self, nested_key: NestedKey) -> None:
        if isinstance(nested_key, str):
            del self._data[nested_key]
        elif isinstance(nested_key, list):
            parent = self._traverse(nested_key[:-1])
            del parent[nested_key[-1]]
        else:
            raise NestedKeyError(f"nested_key must be a str or list, not {type(nested_key)}")
    
    def get(self, nested_path: str, sep: str = '.'):
        """ get a value from a nested path in a dictionary.

        Args:
            nested_path (str): The nested path to traverse.
            sep (str, optional): Defaults to '.'.

        Returns:
            Any: The value at the end of the nested path.

        Examples:
            >>> nd = NestedDict({'a': {'b': {'c': 1}}})
            >>> nd.get('a.b.c')
            1

        """
        path = nested_path.split(sep)
        try:
            return self._traverse(path)
        except KeyError:
            return None
        
    def __iter__(self) -> Iterator:
        return iter(self._data)
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __ne__(self, other: Any) -> bool:
        return self._data != other
    
    def __setitem__(self, nested_key: NestedKey, value: Any) -> None:
        if isinstance(nested_key, str):
            self._data[nested_key] = value
        elif isinstance(nested_key, list):
            dest_key = nested_key[-1]
            parent = self._traverse(nested_key[:-1], construct=True)
            parent[dest_key] = value
        else:
            raise NestedKeyError(f"nested_key must be a str or list, not {type(nested_key)}")
        
    def set(self, nested_path: str, value: Any, sep: str = '.') -> None:
        """ set a value at a nested path in a dictionary.

        Args:
            nested_path (str): The nested path to traverse.
            value (Any): The value to set.
            sep (str, optional): Defaults to '.'.

        Examples:
            >>> nd = NestedDict()
            >>> nd.set('a.b.c', 1)
            >>> nd['a']['b']['c']
            1
            >>> nd.set('a.b.c', 2)
            >>> nd[['a', 'b', 'c']]
            2
        """
        path = nested_path.split(sep)
        self._traverse(path[:-1], construct=True)[path[-1]] = value

    def __str__(self) -> str:
        return f"{__class__.__name__}({str(self._data)})"
    
    def __repr__(self) -> str:
        return f"{__class__.__name__}({repr(self._data)})"
    
    def clear(self) -> None:
        return self._data.clear()

    def copy(self) -> dict:
        return self._data.copy()
    
    def keys(self):
        return self._data.keys()
    
    def values(self):
        return self._data.values()
    
    def items(self):
        return self._data.items()
    
    def to_json(self):
        ...

    def update(self, other: dict):
        self._data.update(other)

