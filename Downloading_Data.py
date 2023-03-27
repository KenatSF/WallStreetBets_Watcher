
import os
import praw
import pandas as pd

def get_data_reddit_hot(word, limit):
    # Stablish connection
    reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                         client_secret=os.getenv("CLIENT_SECRET"),
                         user_agent=os.getenv("USER_AGENT"),
                         username=os.getenv("USERNAME"),
                         password=os.getenv("PASSWORD"))

    reddit.read_only = True

    subreddit = reddit.subreddit(word)

    hotw = subreddit.hot(limit=limit)

    post_ids = []
    df = pd.DataFrame(columns=["id", "created", "title", "body", "stickied", "ups", "downs", "author", "url", "video", "comments_num"])
    comments = pd.DataFrame()

    for post in hotw:
        id = post.id
        created = post.created_utc
        title = post.title
        body = post.selftext
        stickied = post.stickied
        ups = post.ups
        downs = post.downs
        author = post.author
        url = post.url
        video = post.is_video
        comments_num = len(post.comments.list())

        df.loc[df.shape[0]] = [id, created, title, body, stickied, ups, downs, author, url, video, comments_num]

        df_temp = pd.DataFrame()

        all_comments = list()
        # comments = i.comments.list()
        post.comments.replace_more(limit=0)

        for comment in post.comments.list():
            comment_parent = str(comment.parent())
            if comment_parent != id:
                continue
            else:
                comment_id = str(comment.id)
                comment_body = str(comment.body)
                save = "[" + comment_id + ", " + comment_body + "]"
                all_comments.append(save)

        df_temp[id] = all_comments
        comments = pd.concat([comments, df_temp], axis=1)

    return df, comments





