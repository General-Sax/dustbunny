'''adapter_utils.py
Joel Tiura
'''

import pandas as pd

def row_data_to_dataframe(tuple_of_namedtuples):
  column_names = tuple_of_namedtuples[0]._fields
  column_dict = {name: [named_tuple[i] for named_tuple in tuple_of_namedtuples]
                  for i, name in enumerate(column_names)}
  df = pd.DataFrame(data=column_dict)
  return df

