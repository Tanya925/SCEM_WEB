// Main purpose: load publications from the JSON API and handle frontend search and year filtering.

document.addEventListener("DOMContentLoaded", async () => {
    const page = document.querySelector("[data-publication-page]");

    if (!page) {
        return;
    }

    const list = page.querySelector("[data-publication-list]");
    const searchInput = page.querySelector("[data-publication-search]");
    const yearSelect = page.querySelector("[data-publication-year]");
    const totalText = document.querySelector("[data-publication-total]");
    const visibleText = page.querySelector("[data-publication-visible]");
    const loadingText = page.querySelector("[data-publication-loading]");
    const emptyText = page.querySelector("[data-publication-empty]");
    const errorText = page.querySelector("[data-publication-error]");
    const language = document.body.dataset.language || "en";
    let publications = [];

    const hasValue = (value) => value !== null && value !== undefined && String(value).trim() !== "";

    const formatAuthors = (authors) => String(authors || "")
        .split(";")
        .map((author) => author.trim())
        .filter(Boolean)
        .join(", ");

    const formatSource = (publication) => {
        const sourceParts = [];

        if (hasValue(publication.journal)) {
            sourceParts.push(String(publication.journal).trim());
        }

        if (hasValue(publication.publication_year)) {
            sourceParts.push(String(publication.publication_year));
        }

        if (hasValue(publication.volume)) {
            const volume = String(publication.volume);
            const issue = hasValue(publication.issue) ? `(${publication.issue})` : "";
            sourceParts.push(`${volume}${issue}`);
        } else if (hasValue(publication.issue)) {
            sourceParts.push(`(${publication.issue})`);
        }

        if (hasValue(publication.article_number)) {
            sourceParts.push(String(publication.article_number));
        }

        if (hasValue(publication.page)) {
            sourceParts.push(String(publication.page));
        }

        return sourceParts.join(", ");
    };

    const createPublicationCard = (publication, index) => {
        const card = document.createElement("article");
        card.className = "publication-card";
        card.dataset.publicationItem = "";
        card.dataset.year = String(publication.publication_year || "");
        card.dataset.search = [publication.title, publication.authors, publication.journal, publication.publication_year]
            .join(" ")
            .toLowerCase();

        const indexText = document.createElement("span");
        indexText.className = "publication-index";
        indexText.textContent = String(index + 1).padStart(3, "0");

        const content = document.createElement("span");
        content.className = "publication-card-content";

        const title = document.createElement("strong");
        title.className = "publication-title";
        title.textContent = publication.title;

        const authors = document.createElement("span");
        authors.className = "publication-authors";
        authors.textContent = formatAuthors(publication.authors);

        const source = document.createElement("span");
        source.className = "publication-source";
        source.textContent = formatSource(publication);

        const action = document.createElement("a");
        action.className = "publication-open-action";
        action.href = publication.pdf_url;
        action.target = "_blank";
        action.rel = "noopener noreferrer";
        action.setAttribute(
            "aria-label",
            language === "th"
                ? `เปิดแหล่งข้อมูลของผลงานตีพิมพ์: ${publication.title}`
                : `Open source for publication: ${publication.title}`,
        );
        action.innerHTML = `<span>${language === "th" ? "ดูแหล่งข้อมูล" : "View source"}</span><span aria-hidden="true">↗</span>`;

        content.append(title, authors, source);
        card.append(indexText, content, action);
        return card;
    };

    const applyFilters = () => {
        const query = searchInput.value.trim().toLowerCase();
        const selectedYear = yearSelect.value;
        let visibleCount = 0;

        list.querySelectorAll("[data-publication-item]").forEach((item) => {
            const matchesSearch = !query || item.dataset.search.includes(query);
            const matchesYear = selectedYear === "all" || item.dataset.year === selectedYear;
            const isVisible = matchesSearch && matchesYear;
            item.hidden = !isVisible;

            if (isVisible) {
                visibleCount += 1;
                const indexText = item.querySelector(".publication-index");
                if (indexText) {
                    indexText.textContent = String(visibleCount).padStart(3, "0");
                }
            }
        });

        visibleText.textContent = String(visibleCount);
        emptyText.hidden = visibleCount !== 0;
    };

    try {
        const response = await fetch(page.dataset.publicationsUrl, { cache: "no-store" });

        if (!response.ok) {
            throw new Error(`Publication request failed with ${response.status}`);
        }

        publications = await response.json();
        publications.sort((publicationA, publicationB) => {
            const yearA = Number(publicationA.publication_year) || 0;
            const yearB = Number(publicationB.publication_year) || 0;

            if (yearA !== yearB) {
                return yearB - yearA;
            }

            return String(publicationA.title || "").localeCompare(String(publicationB.title || ""));
        });

        if (totalText) {
            totalText.textContent = String(publications.length);
        }

        const years = [...new Set(publications.map((publication) => publication.publication_year).filter(hasValue))]
            .sort((yearA, yearB) => Number(yearB) - Number(yearA));
        years.forEach((year) => {
            const option = document.createElement("option");
            option.value = String(year);
            option.textContent = String(year);
            yearSelect.appendChild(option);
        });

        const fragment = document.createDocumentFragment();
        publications.forEach((publication, index) => {
            fragment.appendChild(createPublicationCard(publication, index));
        });
        list.appendChild(fragment);

        loadingText.hidden = true;
        searchInput.addEventListener("input", applyFilters);
        yearSelect.addEventListener("change", applyFilters);
        applyFilters();
    } catch (error) {
        console.error(error);
        loadingText.hidden = true;
        errorText.hidden = false;
        if (totalText) {
            totalText.textContent = "0";
        }
        visibleText.textContent = "0";
    }
});
