from transformers import pipeline

from collector_db.DTOs.URLWithHTML import URLWithHTML


class HuggingFaceInterface:

    def __init__(self):
        self.pipe = pipeline("text-classification", model="PDAP/url-relevance")

    def get_url_relevancy(
            self,
            urls_with_html: list[URLWithHTML],
            threshold: float = 0.5
    ) -> list[bool]:
        urls = [url_with_html.url for url_with_html in urls_with_html]
        results: list[dict] = self.pipe(urls)

        bool_results = []
        for result in results:
            score = result["score"]
            if score >= threshold:
                bool_results.append(True)
            else:
                bool_results.append(False)
        return bool_results




