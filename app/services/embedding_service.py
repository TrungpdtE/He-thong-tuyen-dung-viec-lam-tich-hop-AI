import hashlib
import math
import re


class EmbeddingService:
    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self._cache: dict[str, list[float]] = {}

    def embed(self, text: str) -> list[float]:
        cached = self._cache.get(text)
        if cached is not None:
            return cached

        vector = [0.0] * self.dimension
        for token in self._tokens(text):
            index = self._stable_hash(token) % self.dimension
            vector[index] += 1.0

        normalized = self._normalize(vector)
        self._cache[text] = normalized
        return normalized

    def similarity(self, text_a: str, text_b: str) -> float:
        vector_a = self.embed(text_a)
        vector_b = self.embed(text_b)
        score = sum(a * b for a, b in zip(vector_a, vector_b))
        return max(0.0, min(1.0, score))

    def _tokens(self, text: str) -> list[str]:
        return re.findall(r"[a-z0-9+#.]+", text.lower())

    def _normalize(self, vector: list[float]) -> list[float]:
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]

    def _stable_hash(self, token: str) -> int:
        return int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)


embedding_service = EmbeddingService()

