def remove_prefix(input_string, prefix):
    if prefix and input_string.startswith(prefix):
        return input_string[len(prefix) :]
    return input_string


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[: -len(suffix)]
    return input_string
