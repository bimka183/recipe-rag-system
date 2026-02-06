import torch
from sentence_transformers import SentenceTransformer

# Проверяем, видит ли Python твою RTX 4060 Ti
device = "cuda" if torch.cuda.is_available() else "cpu"


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('intfloat/multilingual-e5-base', device=device, cache_folder="./cache")

    def get_embedding(self, text_or_list):
        if isinstance(text_or_list, str):
            input_data = ["passage: " + text_or_list]
        else:
            input_data = ["passage: " + t for t in text_or_list]

        embeddings = self.model.encode(input_data, convert_to_numpy=True)

        if isinstance(text_or_list, str):
            return embeddings[0].tolist()
        return embeddings.tolist()
    def get_query_embedding(self, text):
        str =  "query: " + text
        emebedding = self.model.encode(str, convert_to_numpy=True)
        return emebedding.tolist()