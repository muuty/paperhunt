import repository from "./Repository.js";

document.addEventListener("DOMContentLoaded", async () => {
    const searchInput = document.getElementById("search-input");
    const papersContainerId = "papers-container";

    const paperList = new PaperList();
    
    const papers = await repository.loadLatestPapers();
    paperList.fromDatabaseRows(papers);
    paperList.render(papersContainerId);

    const debouncedSearch = debounce(async () => {
        const query = searchInput.value.trim();
        let results;
        if (query.length >= 2) {
            results = await repository.loadLatestPapers();
        paperList.fromDatabaseRows(results);
        paperList.render(papersContainerId);
        }
    }, 500);

    searchInput.addEventListener("input", debouncedSearch);
});