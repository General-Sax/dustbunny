from .linter_class import Linter, TemplateType
from pandas import DataFrame
from typing import Tuple, NamedTuple
from io import StringIO
from pylint import epylint
from



class PyLinter(Linter):
	msg_template = '{line}:{column}:{msg_id}:{msg}:{symbol}'
	score_template = score_template()
	
	
	Score = NamedTuple('Score', ('current', 'previous', 'delta'))
	
	@classmethod
	def score_template(cls) -> TemplateType:
		return (
			('current', float),
	        ('previous', float),
			('delta', float),
		)
	
	@staticmethod
	def run_pylint(target_path: str) -> Tuple[StringIO]:
		cmd = target_path + f" --msg-template={PyLinter.msg_template}"
		stdout, stderr = epylint.py_run(cmd, return_std=True)
		return stdout, stderr
	
	@staticmethod
	def partition_lines(nontrivial_lines: Tuple[str]) -> Tuple[Tuple[str], str]:
		body = nontrivial_lines[1:-2]
		score = nontrivial_lines[-1]
		return body, score
	
	@staticmethod
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
	
	@staticmethod
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
	
	@staticmethod
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
	
	
	


class MypyLinter(ABLinter):
	''''''
	
	def __init__(self, target_path: str):
		self.target_path = target_path
		self.Result = self.__class__.build_result_class()
	
	@classmethod
	def item_template(cls):
		return (
			('line', DataFrame),
			('score', type(None)),
		)
	
	@classmethod
	def result_template(cls):
		return (
			('data', DataFrame),
			('score', type(None)),
		)


('line', int),
('summary', str),


# class Flake8Linter(BaseLinter):
# 	''''''
#
#
# 	class Result(NamedTuple):
# 		placeholder: str
#
# 	def __init__(self, target_path: str):
# 		self.target_path = target_path
# 		self.result = Flake8Linter.Result("\n** flake8 not availalbe **\n")