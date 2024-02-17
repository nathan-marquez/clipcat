from umap import UMAP
import numpy as np


def reduce_embeddings(embeddings):
    if len(embeddings) == 0:
        raise ValueError("Embeddings list is empty.")

    # Adjust n_neighbors based on the dataset size
    n_neighbors = min(
        5, len(embeddings) - 1
    )  # Example adjustment, ensure at least 2 points

    reducer = UMAP(n_components=3, n_neighbors=n_neighbors, random_state=42)

    embeddings_array = np.array(embeddings)
    if embeddings_array.size == 0:
        raise ValueError("Embeddings array is empty after conversion.")

    reduced_embeddings = reducer.fit_transform(embeddings_array)
    return reduced_embeddings.tolist()


# Example usage
# embeddings = [[0.1, 0.2, ...], [...], ...]  # Your embeddings here
# reduced_embeddings = reduce_embeddings_to_3d(embeddings)
# print(reduced_embeddings)


# num_embeddings = 5
# embedding_dim = 512
# random_embeddings = np.random.rand(num_embeddings, embedding_dim)

# random_embeddings.tolist()

# print(reduce_embeddings(random_embeddings))
