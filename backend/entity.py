from datetime import datetime


class ArxivPaper:
    def __init__(
        self,
        id: str,
        title: str,
        authors: str,
        primary_category: str,
        categories: str,
        abstract: str,
        published_at: datetime,
        pdf_url: str,
    ):
        self.id = id
        self.title = title
        self.authors = authors
        self.primary_category = primary_category
        self.categories = categories
        self.abstract = abstract
        self.published_at = published_at
        self.pdf_url = pdf_url


class Summary:
    def __init__(self, research_questions, contributions, experiments):
        self.research_questions = research_questions
        self.contributions = contributions
        self.experiments = experiments


class PaperWithSummary:
    def __init__(
        self,
        arxiv_paper: ArxivPaper,
        summary: Summary,
    ):
        self.arxiv_paper = arxiv_paper
        self.research_questions = summary.research_questions
        self.contributions = summary.contributions
        self.experiments = summary.experiments
