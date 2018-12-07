'''mypy_adapter.py
Joel Tiura
'''
from typing import NamedTuple
from .base_linter import BaseLinter


class MypyLinter(BaseLinter):
    ''''''

    class Result(NamedTuple):
        placeholder: str

    def __init__(self, target_path: str):
        self.target_path = target_path
        self.result = MypyLinter.Result("\n** mypy not availalbe **\n")
