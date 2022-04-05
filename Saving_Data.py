
import os
import praw
import pandas as pd


def compare_existing_id(data_path, data_base_name, comments_base_name, id):
    try:
        os.chdir(data_path)
        df_old = pd.read_csv(data_base_name + ".csv")
        ids = list(df_old["id"])
        if id in ids:
            return True
        else:
            return False
    except:
        os.chdir(data_path)
        df = pd.DataFrame(columns=["id", "created", "title", "body", "stickied", "ups", "downs", "author", "url", "video", "comments_num"])
        df_1 = pd.DataFrame(columns=["First"])
        df.to_csv(data_base_name + ".csv", index=False)
        df_1.to_csv(comments_base_name + ".csv", index=False)
        return False


def get_data_reddit_hot(data_path, data_base_name, comments_base_name, word, limit):
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

    for post in hotw:
        the_id = post.id
        verify = compare_existing_id(data_path, data_base_name, comments_base_name, the_id)
        post_ids.append(the_id)

        os.chdir(data_path)
        if verify:
            id = the_id

            df = pd.read_csv(data_base_name + ".csv")
            df_comments = pd.read_csv(comments_base_name + ".csv")

            df.loc[df.loc[:, "id"] == id, ["ups"]] = post.ups
            df.loc[df.loc[:, "id"] == id, ["downs"]] = post.downs
            df.loc[df.loc[:, "id"] == id, ["comments_num"]] = len(post.comments.list())

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

            df_comments = df_comments.drop(id, 1)

            df_comments = pd.concat([df_comments, df_temp], axis=1)

            df.to_csv(data_base_name + ".csv", index=False)
            df_comments.to_csv(comments_base_name + ".csv", index=False)


        else:
            id = the_id
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


            df = pd.read_csv(data_base_name + ".csv")
            df_comments = pd.read_csv(comments_base_name + ".csv")

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
            df_comments = pd.concat([df_comments, df_temp], axis=1)

            df.to_csv(data_base_name + ".csv", index=False)
            df_comments.to_csv(comments_base_name + ".csv", index=False)
    return post_ids















