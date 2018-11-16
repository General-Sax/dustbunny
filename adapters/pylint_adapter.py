from datetime import datetime
from collections import namedtuple
from itertools import takewhile

import os
import pandas as pd


Score = namedtuple('Score', ('current', 'previous', 'delta'))
PylintItem = namedtuple('PylintItem', ('line', 'error', 'summary', 'description', 'unkn'))


def load_text(path):
    with open(os.path.join(path), 'r') as temp_file:
        text = temp_file.read()
    return text


def text_from_linting_(linting_target_path, temp_file_path=None):
    if temp_file_path is None:
        raw_output_file = os.path.join('./temp_pylint_output.txt')
    else:
        raw_output_file = os.path.join(temp_file_path)
    linting_target = os.path.join(linting_target_path)
    os.system(f'python -m pylint {linting_target} > {raw_output_file}')
    text = load_text(raw_output_file)
    os.system(f'rm {raw_output_file}')
    return text


def lines_of_(text):
    lines = tuple(line.strip() for line in text.strip().split('\n') if line)
    return lines


def partition_(text):
    lines = lines_of_(text)
    header = lines[0]
    body = lines[1:-2]
    score = lines[-1]
    return header, body, score


def extract_score_line_tuple(preprocessed_lines):
    ''''''
    expected_line = preprocessed_lines[-1]
    if (len(expected_line) > 9) and (expected_line[0:9] == "Your code"):
        return tuple(expected_line.split())
    else:
        for line in preprocessed_lines:
            if (len(line) > 9) and (line[0:9] == "Your code"):
                return tuple(line.split())
    raise RuntimeError("no score line was found!")


def string_score_from_(score_line):
    words = score_line.split()
    current = words[6]
    if len(words) == 7:
        previous = None
        delta = None
    else:
        previous = words[9][:-1]
        delta = words[10][:-1]
    score_holder = Score(current, previous, delta)
    return score_holder


def numerical_form_of_(score):
    assert isinstance(score, Score)
    num_score = Score(
        float(score.current.split('/')[0]),
        float(score.previous.split('/')[0]),
        float(score.delta)
    )
    return num_score


def item_list_from_(body_lines):
    ''''''
    colon_split = [line.split(':') for line in body_lines]
    clean_lines = [[entry.strip() for entry in line[1:]] for line in colon_split]
    output = []
    for line in clean_lines:
        if len(line) != 4:
            raise NotImplementedError('No handling for this line format!')

        line_number = line[0]
        unknown = line[1]
        error_code = line[2]
        message = ''.join([char for char in takewhile(lambda x: x != '(', line[3])][:-1])
        concise = line[3].split('(')[-1][:-1]

        final_line = PylintItem(
            line_number,
            error_code,
            concise,
            message,
            unknown
        )
        output.append(final_line)
    return output


def dataframe_from_(pylint_items):
    columns = {
        'LINE': [],
        'ERROR': [],
        'SUMMARY': [],
        'DESCRIPTION': [],
        '???': [],
    }
    for item in pylint_items:
        columns['LINE'].append(item.line)
        columns['ERROR'].append(item.error)
        columns['SUMMARY'].append(item.summary)
        columns['DESCRIPTION'].append(item.description)
        columns['???'].append(item.unkn)
    df = pd.DataFrame(data=columns)
    return df


PylintResult = namedtuple('PylintResult', ('file', 'score', 'data', 'when'))


def lint_file(target_path):
    assert target_path[-3:] == '.py'

    header_line, body_lines, score_line = partition_(text_from_linting_(target_path))
    result = PylintResult(
        target_path,
        numerical_form_of_(string_score_from_(score_line)),
        dataframe_from_(item_list_from_(body_lines)),
        datetime.now().ctime(),
    )
    return result


def quick_test_pipe():
    res = lint_file('./pylint_plugin.py')
    print(res.file)
    print(res.score)
    print(res.when)
    return res.data
