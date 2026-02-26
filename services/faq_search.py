from haystack import Pipeline
from haystack.components.embedders import OpenAITextEmbedder
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever

from services.faq_store import get_faq_store

EMBEDDING_DIM = 1536  # OpenAI text-embedding-3-small
MIN_SCORE = 0.35      # justera vid behov (0.2–0.6)

def get_answer(question: str) -> str | None:
    store = get_faq_store(EMBEDDING_DIM)

    pipe = Pipeline()
    pipe.add_component("text_embedder", OpenAITextEmbedder(model="text-embedding-3-small"))
    pipe.add_component(
        "retriever",
        PgvectorEmbeddingRetriever(document_store=store, top_k=1),
    )
    pipe.connect("text_embedder.embedding", "retriever.query_embedding")

    result = pipe.run({"text_embedder": {"text": question}})
    docs = result["retriever"]["documents"]
    if not docs:
        return None

    best = docs[0]
    score = getattr(best, "score", None)  # Document.score

    if score is None or score < MIN_SCORE:
        return None

    return best.meta.get("answer")

if __name__ == "__main__":
    print(get_answer("When are you open?"))
    print(get_answer("kan man träna rygg?"))