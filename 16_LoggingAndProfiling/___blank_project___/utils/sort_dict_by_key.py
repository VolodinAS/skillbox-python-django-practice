def sort_dict_by_key(dicter: list[dict], key: str) -> list[dict]:
    """
    Сортировка словаря по ключу
    :param key:
    :param dicter:
    :return:
    """
    return sorted(dicter, key=lambda d: d[key])


def sort_dict_by_two_keys(
        lister: list[dict],
        key_1: str,
        key_2: str
):
    # return sorted(lister, key=key)
    return sorted(lister, key=lambda k: (-k[key_1], -k[key_2]))
