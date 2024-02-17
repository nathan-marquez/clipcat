import streamlit as st
import matplotlib.pyplot as plt
from utils.cluster_videos import cluster_videos

st.set_page_config(layout="wide", page_title="Video Clusters Visualization")


def gather_input():
    """
    Gather input from the user for category and number of clusters, and wait for submit button click.
    """
    category = st.text_input("Enter a category:", "mood")
    num_clusters = st.number_input("Number of clusters:", min_value=1, value=3, step=1, max_value=10)
    submitted = st.button('Submit')  # Submit button
    if submitted:
        return show_clusters(category, num_clusters)
    else:
        return None, None  # Return None if not submitted

def show_clusters(category, num_clusters):
    """
    Show clusters visualization based on user input.
    """
    st.title('Video Clusters Visualization')

    clusters_dict = cluster_videos(category, num_clusters)

    # Preparing data for plotting
    labels = list(clusters_dict.keys())
    sizes = [len(videos) for videos in clusters_dict.values()]

    col1, col2 = st.columns(2)  # Creating two columns for side-by-side layout

    with col1:
        st.header('Pie Chart of Video Clusters')
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

    with col2:
        st.header('Bar Graph of Video Clusters')
        fig2, ax2 = plt.subplots()
        ax2.bar(labels, sizes)
        ax2.set_ylabel('Number of Videos')
        ax2.set_title('Videos per Cluster')
        st.pyplot(fig2)