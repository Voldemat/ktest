import re
from typing import Any, Callable, TypeVar, cast

T = TypeVar("T", bound=dict[str, Any])

camel_case_pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake_case(text: str) -> str:
    return camel_case_pattern.sub("_", text).lower()


def change_dict_keys(data: T, func: Callable[[str], str]) -> T:
    new_data: T = cast(T, {})
    for key, value in data.items():
        if isinstance(value, dict):
            new_data[func(key)] = change_dict_keys(value, func)
        elif isinstance(value, list):
            new_array = []
            for v in value:
                if isinstance(v, dict):
                    new_array.append(change_dict_keys(v, func))
                else:
                    new_array.append(v)
            new_data[func(key)] = new_array
        else:
            new_data[func(key)] = value
    return new_data
