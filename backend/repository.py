import logging
import sqlite3

from backend.entity import PaperWithSummary
from backend.query import CREATE_TABLE_QUERY, INSERT_INTO_QUERY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLiteRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_QUERY)
        conn.commit()
        return conn

    def insert_paper(self, paper: PaperWithSummary):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                INSERT_INTO_QUERY,
                (
                    paper.arxiv_paper.id,
                    paper.arxiv_paper.title,
                    paper.arxiv_paper.authors,
                    paper.arxiv_paper.primary_category,
                    paper.arxiv_paper.categories,
                    paper.arxiv_paper.abstract,
                    paper.arxiv_paper.published_at,
                    paper.research_questions,
                    paper.contributions,
                    paper.experiments,
                    paper.arxiv_paper.pdf_url,
                ),
            )

            self.conn.commit()
            logger.info(
                f"✅ Successfully inserted paper: '{paper.arxiv_paper.title}' (ID: {paper.arxiv_paper.id})"
            )

        except Exception as e:
            self.conn.rollback()
            logger.error(
                f"❌ Failed to insert paper: '{paper.arxiv_paper.title}'. Error: {e}"
            )

    def is_paper_already_inserted(self, paper_id: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM papers WHERE id=? LIMIT 1", (paper_id,))
        row = cursor.fetchone()
        return row is not None
