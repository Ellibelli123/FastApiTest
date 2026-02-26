from services.faq_search import get_answer

class FaqHandler:
    async def get_answer(self, question: str) -> str | None:
        # din gamla loop ersätts med semantic search
        return get_answer(question)