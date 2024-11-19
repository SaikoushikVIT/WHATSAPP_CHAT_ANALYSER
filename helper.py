from wordcloud import WordCloud
import emoji
from collections import Counter
import pandas as pd

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    num_messages=df.shape[0]
    words=[]
    for messages in df['message']:
        words.extend(messages.split())

    return num_messages,len(words)
def busy_user(df):
    x=df['user'].value_counts().head()
    return x
def create_wc(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10, background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
def emote(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    timeline1=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline1.shape[0]):
        time.append(timeline1['month'][i]+"-"+ str(timeline1['year'][i]))
    timeline1['time']=time
    return timeline1
def week_activity(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    heatmap1=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heatmap1