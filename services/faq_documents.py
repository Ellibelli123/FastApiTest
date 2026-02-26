from haystack.dataclasses import Document

def faq_to_documents(rows: list[tuple[str, str]]) -> list[Document]:
    docs = []
    for key, value in rows:
        docs.append(
            Document(
                content=f"{key}. {value}",
                meta={"key": key, "answer": value},
            )
        )
    return docs