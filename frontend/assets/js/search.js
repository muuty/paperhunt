import repository from "./Repository.js";

document.addEventListener("DOMContentLoaded", async () => {
  const searchInput = document.getElementById("search-input");
  const papersContainerId = "papers-container";

  const paperList = new PaperList();

  const paperRows = await repository.loadLatestPapers();
  paperList.fromDatabaseRows(paperRows);
  paperList.render(papersContainerId);

  const debouncedSearch = debounce(async () => {
    const query = searchInput.value.trim();
    let paperRows;
    if (query.length >= 2) {
      results = await repository.loadLatestPapers();
      paperList.fromDatabaseRows(paperRows);
      paperList.render(papersContainerId);
    }
  }, 500);

  searchInput.addEventListener("input", debouncedSearch);
});
