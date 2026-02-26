from dotenv import load_dotenv
from haystack.utils import Secret
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

load_dotenv()

def get_faq_store(embedding_dim: int) -> PgvectorDocumentStore:
    return PgvectorDocumentStore(
        connection_string=Secret.from_env_var("PG_CONN_STR"),
        table_name="faq_documents",
        embedding_dimension=embedding_dim,
        vector_function="cosine_similarity",
    )