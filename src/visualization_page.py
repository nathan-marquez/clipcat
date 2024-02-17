import streamlit as st
import plotly.graph_objs as go
import json
from get_video_document_data import get_video_document_data


def load_reduced_vectors(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def plot_3d_vectors(vectors):
    x = []
    y = []
    z = []
    custom_data = []  # Custom data to be used in hover tooltip
    for video_id, vector in vectors.items():
        x.append(vector[0])
        y.append(vector[1])
        z.append(vector[2])
        video_data = get_video_document_data(
            "video" + video_id
        )  # Ensure this matches your data retrieval logic
        # Append title, summary, views, and likes to custom_data for hover information
        custom_data.append(
            (
                video_data["title"],
                video_data["summary"],
                video_data["views"],
                video_data["likes"],
            )
        )

    trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        marker=dict(
            size=5,
            opacity=0.8,
        ),
        customdata=custom_data,
        hovertemplate="<b>%{customdata[0]}<br>Views: %{customdata[2]}<br>Likes: %{customdata[3]}<extra></extra>",
    )

    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
        hovermode="closest",
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig


def show_visualization():
    st.title("3D Visualization of Reduced Document Vectors")
    vectors = load_reduced_vectors("data/reduced_document_vectors.json")
    fig = plot_3d_vectors(vectors)
    st.plotly_chart(fig, use_container_width=True)
