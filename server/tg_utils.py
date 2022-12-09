from datetime import datetime
import pandas as pd

def find_in_list(list_of_objects, value):
    result = next(
        (obj for obj in list_of_objects if obj.word == value),
        None)
    return result

def parse_date(str_date):
    return datetime.strptime(str_date, '%d/%m/%Y')

def fill_gaps(arr):
    df = pd.DataFrame.from_records(arr)
    df = df.groupby('date', as_index=False).sum()
    df['date'] = df['date'].apply(lambda x: parse_date(x))
    r = pd.date_range(start=df.date.min(), end=df.date.max())
    df = df.set_index('date').reindex(r).fillna(0.0).rename_axis('date').reset_index()
    return [{'date': x[0].strftime('%d/%m/%Y'), 'count': x[1]} for x in df.to_numpy()]
