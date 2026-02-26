from haystack import Pipeline
from haystack.components.embedders import OpenAIDocumentEmbedder
from haystack.components.writers import DocumentWriter

from services.faq_documents import faq_to_documents
from services.faq_store import get_faq_store

EMBEDDING_DIM = 1536  # OpenAI text-embedding-3-small

FAQ_ROWS = [
    ("opening hours", "We are open 09-18 on weekdays."),
    ("membership", "You can cancel your membership monthly."),
    ("booking", "You can book a class in the app or at the reception."),
]

def run_index():
    store = get_faq_store(EMBEDDING_DIM)
    docs = faq_to_documents(FAQ_ROWS)

    pipe = Pipeline()
    pipe.add_component("embedder", OpenAIDocumentEmbedder(model="text-embedding-3-small"))
    pipe.add_component("writer", DocumentWriter(document_store=store))
    pipe.connect("embedder.documents", "writer.documents")

    pipe.run({"embedder": {"documents": docs}})

if __name__ == "__main__":
    run_index()
    print("✅ Indexed FAQ documents into pgvector!")