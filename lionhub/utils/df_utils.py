from lionagi import lcall, DataNode
from .sys_utils import timestamp_to_datetime
import pandas as pd
from typing import Dict, List, Any, Dict

def to_pd_df(items: List[Dict], how: str = 'all') -> pd.DataFrame:
    # Converts a list of dicts to a pandas DataFrame, dropping NA values.
    df = pd.DataFrame(items).dropna(how=how)
    df.reset_index(drop=True, inplace=True)
    return df

def pd_row_to_node(row: pd.Series):
    # Converts a pandas Series row to a DataNode object with structured data.
    dict_ = row.to_dict()
    dict_['datetime'] = timestamp_to_datetime(dict_['datetime'])
    dict_['content'] = {'headline': dict_.pop('headline'), 'summary': dict_.pop('summary')}
    dict_['metadata'] = {'datetime': dict_.pop('datetime'), 'url': dict_.pop('url'), 'id': dict_.pop('id')}
    return DataNode.from_dict(dict_)

def expand_df_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df_expanded = df.copy()
    df_expanded['datetime'] = df_expanded['datetime'].apply(lambda x: timestamp_to_datetime(x))

    df_expanded.insert(0, 'year', df_expanded['datetime'].dt.year)
    df_expanded.insert(1, 'month', df_expanded['datetime'].dt.month)
    df_expanded.insert(2, 'day', df_expanded['datetime'].dt.day)
    df_expanded.drop('datetime', axis=1, inplace=True)

    return df_expanded