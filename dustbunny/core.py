from collections import namedtuple
from datetime import datetime
import os

from adapters.pylint_adapter import Pylinter
from adapters.flake8_adapter import Flake8Linter
from adapters.mypy_adapter import MypyLinter


LINTERS = (Pylinter, Flake8Linter, MypyLinter)


def target_filter(target: str) -> str:
    if not os.path.exists(os.path.normpath(target)):
        raise FileNotFoundError(f'Could not find {target}!')
    elif os.path.isdir(target):
        raise NotImplementedError('directory linting not yet supported')
    else:
        return target

# TODO implement concept of Session (relative to target_file?)


class Core:
    ''''''

    def __init__(self, target_path: str):
        self.target_path = target_filter(target_path)
        OpsHost = namedtuple('OpsHost', ['pylint', 'flake8', 'mypy'])
        self.ops = OpsHost(*(linter(target_path) for linter in LINTERS))
        self.last_run_at = datetime.now().ctime()

    def update(self):
        self.last_run_at = datetime.now().ctime()
        for operator in self.ops:
            operator.update()

    def retarget(self, new_target: str):
        self.target_path = target_filter(new_target)
        for operator in self.ops:
            operator.retarget(self.target_path)

    @property
    def results(self):
        results = (operator.result for operator in self.ops)
        return results

    def report(self):
        print(f"\nFILE: {self.target_path}")
        print(f"RUN AT: {self.last_run_at}\n")
        print("*_ pylint _______________________")
        print(self.ops.pylint.report())
        print("*_ flake8 _______________________")
        print(self.ops.flake8.report())
        print("*_ mypy _________________________")
        print(self.ops.mypy.report())
