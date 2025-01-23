import arxiv

from backend.entity import ArxivPaper

MAX_RESULTS = 100


class ArxivCrawler:
    def __init__(self, client: arxiv.Client):
        self.client = client

    def search(self, keyword: str) -> list[ArxivPaper]:
        search = arxiv.Search(
            query=" AND ".join(keyword.split(" ")),
            max_results=1,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )

        return [
            ArxivPaper(
                id=result.entry_id,
                title=result.title,
                authors=",".join([author.name for author in result.authors]),
                primary_category=result.primary_category,
                categories=",".join(result.categories),
                published_at=result.published,
                abstract=result.summary,
                pdf_url=result.pdf_url,
            )
            for result in self.client.results(search)
        ]
