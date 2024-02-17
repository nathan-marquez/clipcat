from openai import OpenAI

client = OpenAI(api_key="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")

index_name = "lecturellamaindex"


def embed_text(text):
    """
    Generate embeddings for the text using the updated OpenAI API.
    """
    response = client.embeddings.create(
        model="text-embedding-ada-002", input=[text]
    )  # Adjust according to the new API if needed)
    # Depending on the new API's response structure, you might need to adjust how you access the embedding
    embedding = response.data[0].embedding
    return embedding
