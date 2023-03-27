from TimeFrame_Periods import get_post_from_n_hours_ago
from WSB_Frequency import get_data_freq
from WSB_Plot import plot_pmi_logfreq
from WSB_Text import cleantext
from Downloading_Data import get_data_reddit_hot
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

def main():
    ## Testing with data saved in data folder
    #my_path = os.getenv("DATA_PATH")
    #os.chdir(my_path)
    ## Getting data
    #df = pd.read_csv("REDDIT.csv")

    # Getting data
    df, comments = get_data_reddit_hot("wallstreetbets", 100)

    # Getting CREATED-POST-DATA from the last n hours ago
    df = get_post_from_n_hours_ago(df, 2)

    # Cleaning data
    df["clean_title"] = df["title"].apply(cleantext)
    df["clean_body"] = df["body"].apply(cleantext)

    # Defining time interval
    time_a = min(list(df["date_time"]))
    time_b = max(list(df["date_time"]))

    new_df = get_data_freq("date_time", time_a, time_b, "clean_body", df)

    print(plot_pmi_logfreq(new_df))

if __name__ == '__main__':
    main()
