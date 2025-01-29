import json
import os
import sys

import arxiv
from dotenv import load_dotenv

from ai import GeminiAI
from crawler import ArxivCrawler
from entity import PaperWithSummary
from repository import SQLiteRepository

load_dotenv()

PAPER_DATABASE_PATH = "papers.db"
GEMINI_API_KEY_PATH = "GEMINI_API_KEY"
MAX_RESULTS = 10


class PaperHuntingJob:
    def __init__(self):
        self.crawler = ArxivCrawler(client=arxiv.Client(), max_results=MAX_RESULTS)
        self.summary_ai = GeminiAI(api_key=os.environ.get(GEMINI_API_KEY_PATH))
        self.repository = SQLiteRepository(db_path=PAPER_DATABASE_PATH)

    def hunt_papers(self, keywords: list[str]):
        for keyword in keywords:
            papers = self.crawler.search(keyword)

            for paper in papers:
                if not self.repository.is_paper_already_inserted(paper.id):
                    summary = self.summary_ai.summarize(paper.pdf_url)
                    self.repository.insert_paper(PaperWithSummary(paper, summary))


if __name__ == "__main__":
    keywords_json = sys.argv[1]
    keywords = json.loads(keywords_json)

    job = PaperHuntingJob()
    job.hunt_papers(keywords)
