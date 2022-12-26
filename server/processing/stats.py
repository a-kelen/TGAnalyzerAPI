def get_count_by_day_for_channel(df):
    grouped_by_day = df.groupby([df['date']])
    res = [{'date': key, 'count': len(mess)} for key, mess in grouped_by_day]
    return res


def get_total_count_for_channel(df):
    return len(df)
