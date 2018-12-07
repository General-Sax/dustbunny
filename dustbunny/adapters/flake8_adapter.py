'''flake8_adapter.py
Joel Tiura
'''
from typing import NamedTuple
from .base_linter import BaseLinter


class Flake8Linter(BaseLinter):
    ''''''

    class Result(NamedTuple):
        placeholder: str

    def __init__(self, target_path: str):
        self.target_path = target_path
        self.result = Flake8Linter.Result("\n** flake8 not availalbe **\n")
