class Paper {
    constructor(id, title, authors, primary_category, categories, abstract, published_at, pdf_url, research_questions, contributions, experiments){
        this.id = id;
        this.title = title;
        this.authors = authors;
        this.primary_category = primary_category;
        this.categories = categories;
        this.abstract = abstract;
        this.published_at = published_at;
        this.pdf_url = pdf_url;
        this.research_questions = research_questions;
        this.contributions = contributions;
        this.experiments = experiments;
    }

    toElement() {
        const container = document.createElement("div");
        container.classList.add("paper-card");

        // arXiv 링크 아이콘 추가
        const arxivLink = document.createElement("a");
        arxivLink.href = this.pdf_url;
        arxivLink.target = "_blank";
        arxivLink.classList.add("arxiv-link");
        arxivLink.title = "View on arXiv";
        arxivLink.innerHTML = "🔗"; // 링크 아이콘

        const categoryContainer = document.createElement("div");
        categoryContainer.classList.add("category-container");
        categoryContainer.appendChild(arxivLink);
        
        JSON.parse(this.categories || "[]").forEach(category => {
            const categoryTag = document.createElement("span");
            categoryTag.classList.add("category-tag");
            categoryTag.textContent = category;
            categoryTag.style.backgroundColor = this.hashColor(category);
            categoryContainer.appendChild(categoryTag);
        });


        container.innerHTML = `
            <div class="paper-contents-container">
                <div class="paper-header">
                    ${categoryContainer.outerHTML}
                    <div class="paper-title-container">
                        <h3 class="paper-title">${this.title}</h3>
                    </div>
                    <span class="paper-date">${this.formatDate(this.published_at)}</span>
                </div>
                <p class="paper-abstract">${this.abstract}</p>
                <div class="paper-details">
                    <h4>Research Questions</h4>
                    <ul>${this.formatList(this.research_questions)}</ul>
                    
                    <h4>Contributions</h4>
                    <ul>${this.formatList(this.contributions)}</ul>
                    
                    <h4>Experiments</h4>
                    <ul>${this.formatList(this.experiments)}</ul>
                </div>
            </div>
            <div class="toggle-bar">▼</div> 
        `;
    
        const toggleButton = container.querySelector(".toggle-bar");
        const details = container.querySelector(".paper-details");
        const abstract = container.querySelector(".paper-abstract");
        
        toggleButton.addEventListener("click", () => {
            const isOpen = details.style.maxHeight;
            if (!isOpen || isOpen === "0px") {
                details.style.maxHeight = details.scrollHeight + "px";
                abstract.classList.add("expanded");
                toggleButton.textContent = "▲";
            } else {
                details.style.maxHeight = "0px";
                abstract.classList.remove("expanded");
                toggleButton.textContent = "▼";
            }
        });
    
        return container;
    }

    hashColor(category) {
        let hash = 0;
        for (let i = 0; i < category.length; i++) {
            hash = category.charCodeAt(i) + ((hash << 5) - hash);
        }
        const hue = Math.abs(hash) % 360; 
        return `hsl(${hue}, 60%, 75%)`;
    }

    formatList(data) {
        /*
            FIXME: Can be simplified if the data is formatted as an json string.

            ex) data = "-keyword1:description1\n- keyword2:description2"
            to <li>keyword1: description1</li><li>keyword2: description2</li> 
        */
        return data
            .split("\n")
            .map(line => line.trim())
            .filter(line => line)
            .map(line => {
                const content = line.startsWith("-") ? line.slice(1).trim() : line;
                return `<li>${content}</li>`;
            })
            .join("");
    };

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toISOString().split("T")[0];
    }
}
