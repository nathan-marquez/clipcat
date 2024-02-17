from pinecone import Pinecone, ServerlessSpec
import os
import json
from embed_text import embed_text

# Initialize your OpenAI and Pinecone credentials
pc = Pinecone(api_key="95cbf918-f4f3-4c2c-8701-cc953c55fce7")

# Name of your index
index_name = "mockclipcat"

# Connect to the index
index = pc.Index(
    name=index_name,
    host="https://mockclipcat-6h75lpv.svc.gcp-starter.pinecone.io",
)


def upload_text_to_pinecone(text, name):
    embedding = embed_text(text)
    # Generate a unique ID for each document
    doc_id = name
    # Insert into Pinecone
    index.upsert(vectors=[(doc_id, embedding)])
    return doc_id


def prep_rag(directory="../data/video_documents"):
    """
    Checks file type, processes file content accordingly, generates embeddings, and uploads to Pinecone.
    """
    # List all files in the specified directory
    files = os.listdir(directory)

    for file in files:
        # Construct the full file path
        file_path = os.path.join(directory, file)

        # Check if the file is a .json file
        if file.endswith(".json"):
            # Open and load the JSON file
            with open(file_path, "r") as json_file:
                data = json.load(json_file)

                # Process transcript_chunks
                if "transcript_chunks" in data:
                    for chunk_id, chunk_text in data["transcript_chunks"].items():
                        name = f"{os.path.splitext(file)[0]}_chunk{chunk_id}"
                        upload_text_to_pinecone(chunk_text, name)

                # Process scene_captions
                if "scene_captions" in data:
                    for scene_id, scene_text in data["scene_captions"].items():
                        name = f"{os.path.splitext(file)[0]}_scene{scene_id}"
                        upload_text_to_pinecone(scene_text, name)


# Call the function to process and upload data
prep_rag()
