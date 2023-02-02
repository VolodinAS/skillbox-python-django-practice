import os.path
from os.path import dirname


def get_fake_file(file_name: str):
    tests_dir = dirname(dirname(__file__))
    tests_dir = os.path.join(tests_dir, 'files')
    test_file = os.path.join(tests_dir, file_name)
    if os.path.exists(test_file):
        return test_file
    return False
