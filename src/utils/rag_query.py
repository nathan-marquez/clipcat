from pinecone import Pinecone
import os
import json
from embed_text import embed_text

# Assume Pinecone and embed_text are properly initialized and imported
pc = Pinecone(api_key="95cbf918-f4f3-4c2c-8701-cc953c55fce7")
index_name = "mockclipcat"
index = pc.Index(
    name=index_name,
    host="https://mockclipcat-6h75lpv.svc.gcp-starter.pinecone.io",
)


def embed_query(query):
    # This function should return the embedding of the query
    return embed_text(query)


def search_pinecone(embedded_query, top_k=10):
    # This function searches the Pinecone index and returns the top k results
    # Ensure that the query is properly formatted
    # Specifically, the vectors parameter should be a list of vectors, without mixing IDs in the query payload
    try:
        response = index.query(vector=embedded_query, top_k=top_k)
        return response
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return []


def get_video_document_ids(matching_documents):
    # This extracts video document ids from the matching documents' ids
    video_ids = set()
    for doc in matching_documents:
        video_id = doc.split("_")[
            0
        ]  # Assuming the doc ID format is "mockvideo<id>_chunk/scene<chunk/sceneid>"
        video_ids.add(video_id)
    return list(video_ids)


def load_video_documents(video_ids, directory="../data/video_documents"):
    # This function loads the video documents based on the video ids
    video_documents = []
    for video_id in video_ids:
        file_path = os.path.join(directory, f"{video_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                video_documents.append(json.load(file))
    return video_documents


def rag_query(query):
    embedded_query = embed_query(query)
    search_results = search_pinecone(embedded_query)
    print(search_results)
    matches = search_results["matches"]
    matching_documents = [result["id"] for result in matches]

    video_ids = get_video_document_ids(matching_documents)
    video_ids = list(set(video_ids))
    video_documents = load_video_documents(video_ids)

    ragged_query = "You are a youtube channel question answering bot. I will provide you some context of a few of the channels videos, but not all of them, they are only a subset that are related to the user's query. Respond as the question answering chatbot using this limited subset of youtube channel information: "
    for doc in video_documents:
        ragged_query += json.dumps(doc) + " \n"

    ragged_query += "\n\n\n\nThis is the user's query: " + query
    return ragged_query


# Save this function in a file named rag_query.py


query = input("ask a question:")
ragged = rag_query(query)
print("NEW QUERY")
print(ragged)
