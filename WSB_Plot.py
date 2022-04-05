import plotly.express as px

def plot_pmi_logfreq(database):
    df = database

    fig = px.scatter(x=df['PMI'].values, y=df['log(bi_gram_freq)'].values, color=df['PMI'] + df['log(bi_gram_freq)'],
                     size=(df['PMI'] + df['log(bi_gram_freq)']).apply(lambda x: 1 / (1 + abs(x))).values,
                     hover_name=df['bi_gram'].values, width=600, height=600,
                     labels={'x': 'PMI', 'y': 'Log(Bigram Frequency)'})
    fig.show()

    return df.loc[(df["PMI"] > -5) & (df["log(bi_gram_freq)"] >= 1), ["bi_gram"]]


