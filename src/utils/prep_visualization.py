import os
import json
from embed_text import embed_text
from reduce_embeddings import reduce_embeddings


def prep_visualization():
    # Directory where mock video documents are stored
    documents_dir = "../data/video_documents"
    output_file = "../data/reduced_document_vectors.json"

    # Placeholder for embeddings and document ids
    embeddings = []
    document_ids = []

    # Iterate over video document files
    for filename in os.listdir(documents_dir):
        print(filename)
        if filename.startswith("mockvideo") and filename.endswith(".json"):
            filepath = os.path.join(documents_dir, filename)
            with open(filepath, "r") as file:
                video_document = json.load(file)
                # Assuming the text content to embed is under a key named "text"
                document_string = json.dumps(video_document, sort_keys=True)
                # Generate embedding for the document text
                embedding = embed_text(document_string)
                embeddings.append(embedding)
                # Extract document id from filename, assuming the format "mockvideo{id}.json"
                document_id = filename.replace("mockvideo", "").replace(".json", "")
                document_ids.append(document_id)

    reduced_embeddings = reduce_embeddings(embeddings)

    # Create a mapping from video document id to the 3D vector
    document_to_vector_mapping = {
        document_id: vector
        for document_id, vector in zip(document_ids, reduced_embeddings)
    }

    # Write the mapping to a JSON file
    with open(output_file, "w") as out_file:
        json.dump(document_to_vector_mapping, out_file)

    print(f"Reduced embeddings written to {output_file}")


# Call the function
prep_visualization()
