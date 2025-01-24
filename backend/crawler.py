import json

import arxiv

from backend.entity import ArxivPaper

ARXIV_TEXONOMY = json.loads(open("./arxiv_texonomy.json", "r").read())


class ArxivCrawler:
    def __init__(self, client: arxiv.Client, max_results: int):
        self.client = client
        self.max_results = max_results

    def search(self, keyword: str) -> list[ArxivPaper]:
        search = arxiv.Search(
            query=" AND ".join(keyword.split(" ")),
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )

        return [
            ArxivPaper(
                id=result.entry_id,
                title=result.title,
                authors=json.dumps([author.name for author in result.authors]),
                primary_category=ARXIV_TEXONOMY.get(
                    result.primary_category, result.primary_category
                ),
                categories=json.dumps(
                    [
                        ARXIV_TEXONOMY.get(category, category)
                        for category in result.categories
                    ]
                ),
                published_at=result.published,
                abstract=result.summary,
                pdf_url=result.pdf_url,
            )
            for result in self.client.results(search)
        ]
