'''pylint_adapter.py
Joel Tiura
'''
from io import StringIO
from collections import namedtuple
from typing import Tuple  # List, , Optional, Dict, Union
from pylint import epylint
from .op_utilities import stringio_clean, row_data_to_dataframe


PylintResult = namedtuple('PylintResult', ('score', 'data'))
Score = namedtuple('Score', ('current', 'previous', 'delta'))
PylintItem = namedtuple('PylintItem', ('line', 'column', 'error', 'summary', 'description'))

MSG_TEMPLATE = '{line}:{column}:{msg_id}:{msg}:{symbol}'


def run_pylint(target_path: str) -> Tuple[StringIO]:
    cmd = target_path + f" --msg-template={MSG_TEMPLATE}"
    stdout, stderr = epylint.py_run(cmd, return_std=True)
    return stdout, stderr


def partition_lines(nontrivial_lines: Tuple[str]) -> Tuple[Tuple[str], str]:
    body = nontrivial_lines[1:-2]
    score = nontrivial_lines[-1]
    return body, score


def extract_score_data(score_line: str) -> Score:
    words = score_line.split()
    current = words[6]
    if len(words) == 7:
        previous = None
        delta = None
    else:
        previous = words[9][:-1]
        delta = words[10][:-1]
    score_data = Score(
        float(current.split('/')[0]),
        float(previous.split('/')[0]) if previous else None,
        float(delta) if delta else None,
    )
    return score_data


def parse_pylint_body_lines(body_lines: Tuple[str]) -> Tuple[PylintItem]:
    '''
    '''
    colon_split = (line.split(':') for line in body_lines)
    clean_lines = ([entry.strip() for entry in line] for line in colon_split)
    item_list = []
    for line in clean_lines:
        if len(line) != 5:
            raise ValueError(f'No handling for this line format: {line}')
        line_number = line[0]
        column = line[1]
        error = line[2]
        summary = line[4]
        description = line[3]
        item = PylintItem(
            line_number,
            column,
            error,
            summary,
            description
        )
        item_list.append(item)
    output = tuple(item_list)
    return output


def process_pylint_stdout(pylint_stdout: StringIO) -> PylintResult:
    '''
    '''
    clean_lines = stringio_clean(pylint_stdout)
    raw_body, raw_score = partition_lines(clean_lines)
    body = parse_pylint_body_lines(raw_body)
    score = extract_score_data(raw_score)
    data = row_data_to_dataframe(body, PylintItem)
    result = PylintResult(score, data)
    return result
    


class Pylinter:
    msg_template = MSG_TEMPLATE

    def __init__(self, target_path: str) -> type(None):
        self.target_path = target_path
        self.result = None
        self.update()

    # update - core function
    def retarget(self, new_target: str):
        self.target_path = new_target
        self.update()

    # update - API function
    def update(self) -> type(None):
        stdout, stderr = run_pylint(self.target_path)
        # TODO Processing for stderr?
        self._result = process_pylint_stdout(stdout)

    def report(self):
        if self.result is None:
            self.update()
        report_text = '\n' + f'{self.data}\n'
        report_text += '\n' + f'SCORE'
        report_text += '\n' + f' CURRENT: {self.score.current}'
        report_text += '\n' + f'PREVIOUS: {self.score.previous}'
        report_text += '\n' + f'  CHANGE: {self.score.delta}\n'
        return report_text

    def other_report(self):
        if self.result is None:
            self.update()
        df = self.data.LINE
        df = df.append(self.data.SUMMARY)
        report_text = '\n' + f'{str(df)}\n'
        # report_text += '\n' + f'SCORE'
        # report_text += '\n' + f' CURRENT: {self.score.current}'
        # report_text += '\n' + f'PREVIOUS: {self.score.previous}'
        # report_text += '\n' + f'  CHANGE: {self.score.delta}\n'
        return report_text

    @property
    def data(self):
        if self.result is None:
            return None
        return self.result.data

    @property
    def score(self):
        if self.result is None:
            return None
        return self.result.score
