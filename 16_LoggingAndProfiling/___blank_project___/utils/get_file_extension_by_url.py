from pprint import pprint

import urllib3
from urllib3.util import Url


def get_file_extension_by_url(url: str) -> str:
    data_url: Url = urllib3.util.parse_url(url)
    request_data: str = data_url.request_uri
    request_list: list = request_data.split('?')
    request_list: list = request_list[0].split('.')
    print(f'{request_list=}')

    return request_list[-1]
