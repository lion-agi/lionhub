import pandas as pd
from lionagi import DataNode
from .sys_utils import timestamp_to_datetime

def to_pd_df(items, how='all'):
    df = pd.DataFrame(items).dropna(how=how)
    df.reset_index(drop=True, inplace=True)
    return df

def expand_df_datetime(df):
    df_ = df.copy()
    df_['datetime'] = [timestamp_to_datetime(i) for i in df_['datetime']]
    
    year = [i.year for i in df_['datetime']]
    month = [i.month for i in df_['datetime']]
    day = [i.day for i in df_['datetime']]
    
    df_.insert(0, 'year', year)
    df_.insert(1, 'month', month)
    df_.insert(2, 'day', day)
    df_.pop('datetime')
    return df_

def pd_row_to_node(row):
    dict_ = row.to_dict()
    dict_['datetime'] = timestamp_to_datetime(dict_['datetime'])
    dict_['content'] = {
        'headline': dict_.pop('headline'), 
        'summary': dict_.pop('summary')
        }
    dict_['metadata'] = {
        'datetime': dict_.pop('datetime'), 
        'url': dict_.pop('url'), 
        'id': dict_.pop('id')
        }
    return DataNode.from_dict(dict_)
