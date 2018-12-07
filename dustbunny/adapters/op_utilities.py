'''op_utilities.py
Joel Tiura
'''
from glob import glob
# from datetime import datetime
# import os

from numpy.random import choice
import pandas as pd


def rand_target():
    targets = glob('./**/*.py', recursive=True)
    return choice(targets).replace("\\", "/")


def stringio_clean(stringio):
    lines = tuple(stringio.read().strip().split('\n'))
    stripped = (line.strip() for line in lines)
    filtered = tuple(line for line in stripped if line)
    return filtered


def row_data_to_dataframe(tuple_of_namedtuples, item_class):
    column_names = item_class._fields
    column_dict = {name.upper(): [named_tuple[i] for named_tuple in tuple_of_namedtuples]
                   for i, name in enumerate(column_names)}
    data = pd.DataFrame(data=column_dict)
    return data
