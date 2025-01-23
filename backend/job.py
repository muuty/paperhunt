import os

import arxiv
from dotenv import load_dotenv

from backend.ai import GeminiAI
from backend.crawler import ArxivCrawler
from backend.entity import PaperWithSummary
from backend.repository import SQLiteRepository

load_dotenv()

PAPER_DATABASE_PATH = "papers.db"
GEMINI_API_KEY_PATH = "GEMINI_API_KEY"


class PaperHuntingJob:
    def __init__(self):
        self.crawler = ArxivCrawler(client=arxiv.Client())
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
    job = PaperHuntingJob()
    job.hunt_papers(["traffic prediction"])
