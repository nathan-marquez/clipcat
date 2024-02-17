from transformers import CLIPProcessor, CLIPModel
import torch

# Initialize the model and processor globally to avoid reloading them on each function call
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def embed_text(text):
    """
    Embeds the input text using the CLIP model and returns the embedding vector.

    Parameters:
    - text (str): The text to embed.

    Returns:
    - A PyTorch tensor representing the embedded text.
    """
    # Process the text to be compatible with the CLIP model
    inputs = processor(text=text, return_tensors="pt", padding=True, truncation=True)

    # Generate embeddings
    with torch.no_grad():  # Ensure no gradients are calculated
        embeddings = model.get_text_features(**inputs)

    return embeddings.tolist()[0]
