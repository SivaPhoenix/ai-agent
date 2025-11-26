# vector_store.py
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class VectorStore:
    def __init__(self):
        self.docs = {}  # key -> text
        self.keys = []
        self._vectorizer = None
        self._matrix = None

    def upsert(self, key, obj):
        text = ""
        if isinstance(obj, dict):
            # store brief + variants if present
            text = (obj.get("brief", {}).get("headline_suggestion","") or "") + " " + str(obj.get("variants",""))
        else:
            text = str(obj)
        self.docs[key] = text
        self._rebuild()

    def upsert_embedding(self, key, text):
        self.upsert(key, text)

    def _rebuild(self):
        texts = list(self.docs.values())
        if not texts:
            self._vectorizer = None
            self._matrix = None
            self.keys = []
            return
        self._vectorizer = TfidfVectorizer(max_features=5000).fit(texts)
        self._matrix = self._vectorizer.transform(texts).toarray()
        self.keys = list(self.docs.keys())

    def query_similar(self, query_text, k=3):
        if self._vectorizer is None:
            return []
        qv = self._vectorizer.transform([query_text]).toarray()[0]
        sims = []
        for i, vec in enumerate(self._matrix):
            score = float(np.dot(qv, vec) / (np.linalg.norm(qv) * (np.linalg.norm(vec) + 1e-9) + 1e-9))
            sims.append((self.keys[i], score))
        sims.sort(key=lambda x: x[1], reverse=True)
        return sims[:k]
