
from datetime import datetime, timedelta
import os
import pandas as pd

# DATE
def timestamp_specific_hour(fecha):
    return datetime.fromtimestamp(fecha)

def timestamp_rounding_hour(fecha):
    return datetime.fromtimestamp(fecha).replace(second=0, minute=0)

def get_post_from_n_hours_ago(data_base, n_hours):
    df = data_base

    time_now = datetime.now()
    time_past = time_now - timedelta(hours=n_hours, minutes=0)

    time_now = time_now.replace(minute=0, second=0)
    time_past = time_past.replace(minute=0, second=0)

    time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")
    time_past = time_past.strftime("%Y-%m-%d %H:%M:%S")

    df["date_time"] = df["created"].apply(timestamp_rounding_hour)
    #df["hour"] = df["created"].apply(timestamp_specific_hour)
    #df = df_reddit.loc[df_reddit["id"].isin(ids), :]

    df_filtered = df.loc[(df["date_time"] >= time_past) & (df["date_time"] <= time_now), :]

    return df_filtered



def get_hot_reddit(path, id_database, reddit_database):
    os.chdir(path)
    df_id = pd.read_csv(id_database)
    ids = list(df_id["ids"])
    df_reddit = pd.read_csv(reddit_database)

    df_reddit["date_hour"] = df_reddit["created"].apply(timestamp_specific_hour)
    df_reddit["date"] = df_reddit["created"].apply(timestamp_rounding_hour)

    df = df_reddit.loc[df_reddit["id"].isin(ids), :]

    return df

