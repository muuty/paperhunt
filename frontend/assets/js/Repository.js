class Repository {
    static instance;

    constructor(dbPath = "/assets/db/papers.db") {
        if (Repository.instance) return Repository.instance;
        this.db = null;
        this.dbPath = dbPath;
        this.initPromise = this._initDb(); // DB 초기화 후 Promise 저장
        Repository.instance = this;
    }

    async _initDb() {
        if (this.db) return;

        const SQL = await initSqlJs({
            locateFile: filename => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${filename}`
        });

        const response = await fetch(this.dbPath);
        const buffer = await response.arrayBuffer();
        this.db = new SQL.Database(new Uint8Array(buffer));

        console.log("Database loaded successfully");
    }

    async loadLatestPapers() {
        await this.initPromise; // DB가 완전히 로드될 때까지 대기
        if (!this.db) return [];

        const stmt = this.db.prepare("SELECT * FROM papers ORDER BY published_at DESC");
        let papers = [];

        while (stmt.step()) {
            papers.push(stmt.getAsObject());
        }
        stmt.free();

        return papers;
    }

    async searchPapers(query) {
        await this.initPromise;
        if (!this.db || query.length < 2) return [];

        const stmt = this.db.prepare("SELECT * FROM papers WHERE title LIKE ? OR abstract LIKE ? ORDER BY published_at DESC");
        stmt.bind([`%${query}%`, `%${query}%`]);

        let papers = [];
        while (stmt.step()) {
            papers.push(stmt.getAsObject());
        }
        stmt.free();

        return papers;
    }
}

const repository = new Repository();
export default repository;