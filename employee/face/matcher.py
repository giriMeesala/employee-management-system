import numpy as np


def cosine_similarity(embedding1, embedding2):

    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)

    similarity = np.dot(
        embedding1,
        embedding2
    ) / (

        np.linalg.norm(embedding1) *
        np.linalg.norm(embedding2)

    )

    return similarity


def is_same_person(
        embedding1,
        embedding2,
        threshold=0.60
):

    similarity = cosine_similarity(
        embedding1,
        embedding2
    )

    print(f"Similarity : {similarity}")

    return similarity >= threshold