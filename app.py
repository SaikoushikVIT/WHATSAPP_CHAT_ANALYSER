import prep,helper
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analysis")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=prep.preprocess(data)
    user_list=df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Analyze"):
        num_messages,words=helper.fetch_stats(selected_user,df)
        col1,col2=st.columns(2)
        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total no of words")
            st.title(words)

        st.title("Active Timeline")
        timeline1=helper.timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline1['time'],timeline1['message'],color='red')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.title("week timeline")
        col1,col2= st.columns(2)
        with col1:
            st.header("busy days")
            busy_day=helper.week_activity(selected_user,df)
            fig, ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='red')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col2:
            st.header('Busy Months')
            busy_month=helper.week_activity(selected_user,df)
            fig, ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='blue')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        if selected_user=="Overall":
            st.title("Most busy User")
            x=helper.busy_user(df)
            fig, ax =plt.subplots()
            ax.bar(x.index, x.values,color='red')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        st.title("Most Used Words")
        df_wc=helper.create_wc(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        emoji_df=helper.emote(selected_user,df)
        st.title("Emoji analysis")

        col1,col2=st.columns(2)
        with col1:
            formatted_output = emoji_df.head(10).to_string(index=False, header=False)
            st.text(formatted_output)
        with col2:
            fig, ax=plt.subplots()
            ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10), autopct='%1.1f%%')
            st.pyplot(fig)

        st.title("activity heat map")
        heatmap1 = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(heatmap1)
        st.pyplot(fig)
