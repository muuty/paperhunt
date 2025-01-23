CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS papers (
        id TEXT NOT NULL PRIMARY KEY,
        title TEXT NOT NULL,
        authors TEXT,
        primary_category TEXT,
        categories TEXT,
        abstract TEXT,
        published_at TEXT,
        research_questions TEXT,
        contributions TEXT,
        experiments TEXT,
        pdf_url TEXT
    )"""

INSERT_INTO_QUERY = """
    INSERT INTO papers
    (id, title, authors, primary_category, categories, abstract, published_at,
     research_questions, contributions, experiments, pdf_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
