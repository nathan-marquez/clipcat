import streamlit as st
import plotly.graph_objs as go
import json


# Function to load the reduced document vectors from JSON
def load_reduced_vectors(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


# Function to create a 3D plot of the vectors
def plot_3d_vectors(vectors):
    x = [v[0] for v in vectors.values()]
    y = [v[1] for v in vectors.values()]
    z = [v[2] for v in vectors.values()]
    ids = list(vectors.keys())

    trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers+text",
        marker=dict(
            size=5,
            opacity=0.8,
        ),
        text=ids,
        textposition="top center",
    )

    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig


# Streamlit app
def main():
    st.title("3D Visualization of Reduced Document Vectors")

    # Load the reduced document vectors
    vectors = load_reduced_vectors("data/reduced_document_vectors.json")

    # Plot the vectors
    fig = plot_3d_vectors(vectors)
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
