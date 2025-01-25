class PaperList {
    constructor() {
        this.papers = [];
    }

    setPapers(papers) {
        this.papers = papers;
    }

    convertRowToPaper(row) {
        return new Paper(
            row.id,
            row.title,
            row.authors,
            row.primary_category,
            row.categories,
            row.abstract,
            row.published_at,
            row.pdf_url,
            row.research_questions,
            row.contributions,
            row.experiments
        );
    }

    fromDatabaseRows(rows) {
        this.papers = rows.map((row) => this.convertRowToPaper(row));
    }

    render(containerId) {
        const container = document.getElementById(containerId);
        container.innerHTML = "";
        this.papers.forEach((paper) => {
            container.appendChild(paper.toElement());
        });
    }
}