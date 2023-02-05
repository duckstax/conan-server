from collections.abc import Iterable


def check_if_numbers_are_consecutive(list_):
    return all(
        True if second - first == 1 else False
        for first, second in zip(list_[:-1], list_[1:])
    )


def _construct_key(previous_key, separator, new_key, replace_separators=None):
    if replace_separators is not None:
        new_key = str(new_key).replace(separator, replace_separators)
    if previous_key:
        return u"{}{}{}".format(previous_key, separator, new_key)
    else:
        return new_key


def flatten(
        nested_dict,
        separator="_",
        root_keys_to_ignore=None,
        replace_separators=None):
    assert isinstance(nested_dict, dict), "flatten requires a dictionary input"
    assert isinstance(separator, str), "separator must be string"

    if root_keys_to_ignore is None:
        root_keys_to_ignore = set()

    if len(nested_dict) == 0:
        return {}

    # This global dictionary stores the flattened keys and values and is
    # ultimately returned
    flattened_dict = dict()

    def _flatten(object_, key):
        # Empty object can't be iterated, take as is
        if not object_:
            flattened_dict[key] = object_
        # These object types support iteration
        elif isinstance(object_, dict):
            for object_key in object_:
                if not (not key and object_key in root_keys_to_ignore):
                    _flatten(
                        object_[object_key],
                        _construct_key(
                            key,
                            separator,
                            object_key,
                            replace_separators=replace_separators))
        elif isinstance(object_, (list, set, tuple)):
            for index, item in enumerate(object_):
                _flatten(
                    item,
                    _construct_key(
                        key,
                        separator,
                        index,
                        replace_separators=replace_separators))
        # Anything left take as is
        else:
            flattened_dict[key] = object_

    _flatten(nested_dict, None)
    return flattened_dict


def _unflatten_asserts(flat_dict, separator):
    assert isinstance(flat_dict, dict), "un_flatten requires dictionary input"
    assert isinstance(separator, str), "separator must be string"
    assert all((not value or not isinstance(value, Iterable) or
                isinstance(value, str)
                for value in flat_dict.values())), "provided dict is not flat"


def unflatten(flat_dict, separator='_'):
    _unflatten_asserts(flat_dict, separator)

    # This global dictionary is mutated and returned
    unflattened_dict = dict()

    def _unflatten(dic, keys, value):
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})

        dic[keys[-1]] = value

    list_keys = sorted(flat_dict.keys())
    for i, item in enumerate(list_keys):
        if i != len(list_keys) - 1:
            split_key = item.split(separator)
            next_split_key = list_keys[i + 1].split(separator)
            if not split_key == next_split_key[:-1]:
                _unflatten(unflattened_dict, item.split(separator),
                           flat_dict[item])
            else:
                pass  # if key contained in next key, json will be invalid.
        else:
            #  last element
            _unflatten(unflattened_dict, item.split(separator),
                       flat_dict[item])
    return unflattened_dict


#flatten



class Document(dict):
    def __init__(self, doc_id):
        super().__init__()
        self.update({"doc_id": doc_id})


class IndexInDisk:
    def __init__(self):
        self.metadata = dict()
        self.key_value = dict()

    def insert(self, key, value):



class IndexInMemory:
    def __init__(self):
        self.base_index = dict()

    def insert(self, key, value: document):
        self.base_index[key] = value


class Index:
    def __init__(self):
        self.index_in_disk = index_in_disk()
        self.index_in_memory = index_in_memory()

    def insert(self, key, value):
        self.index_in_memory.insert(key, value)
        self.index_in_disk.key_value[key] = value


if __name__ == '__main__':
    index = Index()
    index.insert("key", Document("doc"))
