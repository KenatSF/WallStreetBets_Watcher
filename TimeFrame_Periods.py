
from datetime import datetime, timedelta

# DATE
def timestamp_specific_hour(fecha):
    return datetime.fromtimestamp(fecha)

def timestamp_round_hour(fecha):
    return datetime.fromtimestamp(fecha).replace(second=0, minute=0)

def get_post_from_n_hours_ago(data_base, n_hours):
    df = data_base

    time_now = datetime.now()
    time_past = time_now - timedelta(hours=n_hours, minutes=0)

    time_now = time_now.replace(minute=0, second=0)
    time_past = time_past.replace(minute=0, second=0)

    time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")
    time_past = time_past.strftime("%Y-%m-%d %H:%M:%S")

    df["hour"] = df["created"].apply(timestamp_round_hour)
    #df["hour"] = df["created"].apply(timestamp_specific_hour)
    #df = df_reddit.loc[df_reddit["id"].isin(ids), :]

    df_filtered = df.loc[(df["hour"] >= time_past) & (df["hour"] <= time_now), :]

    return df_filtered




