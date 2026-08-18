// Main purpose: control the main public-site interactions and visual behavior.

document.addEventListener("DOMContentLoaded", () => {
    const normalizeFilterValue = (value) => String(value || "")
        .toLowerCase()
        .replace(/\s+/g, " ")
        .trim();

    const menuToggle = document.querySelector("[data-menu-toggle]");
    const menuPanel = document.querySelector("[data-menu-panel]");

    if (menuToggle && menuPanel) {
        menuToggle.addEventListener("click", () => {
            const isOpen = menuPanel.classList.toggle("is-open");
            menuToggle.setAttribute("aria-expanded", String(isOpen));
        });
    }

    const revealCards = document.querySelectorAll(".reveal-card");

    if ("IntersectionObserver" in window && revealCards.length > 0) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    revealObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.15
        });

        revealCards.forEach((card) => revealObserver.observe(card));
    } else {
        revealCards.forEach((card) => card.classList.add("is-visible"));
    }

    const positionFilter = document.querySelector("[data-staff-filter-position]");
    const departmentFilter = document.querySelector("[data-staff-filter-department]");
    const staffSearchInput = document.querySelector("[data-staff-search]");
    const staffEmptyText = document.querySelector("[data-staff-empty]");
    const staffCards = document.querySelectorAll("[data-staff-card]");
    const staffSections = document.querySelectorAll("[data-staff-section]");
    const staffListSection = document.querySelector(".staff-list-section");

    if (staffCards.length > 0 && (positionFilter || departmentFilter || staffSearchInput)) {
        const applyStaffFilters = () => {
            const selectedPosition = positionFilter ? normalizeFilterValue(positionFilter.value) : "all";
            const selectedDepartment = departmentFilter
                ? normalizeFilterValue(departmentFilter.value)
                : "all";
            const searchQuery = staffSearchInput ? staffSearchInput.value.trim().toLowerCase() : "";
            let totalVisibleCards = 0;

            staffCards.forEach((card) => {
                const positionValue = normalizeFilterValue(card.dataset.position);
                const departmentValue = normalizeFilterValue(card.dataset.department);
                const searchText = card.dataset.search || card.textContent.toLowerCase();

                const matchesPosition = selectedPosition === "all" || positionValue === selectedPosition;
                const matchesDepartment = selectedDepartment === "all" || departmentValue === selectedDepartment;
                const matchesSearch = searchQuery === "" || searchText.includes(searchQuery);
                const isVisible = matchesPosition && matchesDepartment && matchesSearch;

                card.hidden = !isVisible;

                if (isVisible) {
                    totalVisibleCards += 1;
                }
            });

            staffSections.forEach((section) => {
                const visibleCards = section.querySelectorAll("[data-staff-card]:not([hidden])");
                section.hidden = visibleCards.length === 0;
            });

            if (staffEmptyText) {
                staffEmptyText.hidden = totalVisibleCards > 0;
            }

            if (staffListSection) {
                const hasSearchState = searchQuery !== "" || selectedPosition !== "all" || selectedDepartment !== "all";
                staffListSection.classList.toggle("is-empty-search", hasSearchState && totalVisibleCards === 0);
            }
        };

        positionFilter?.addEventListener("change", applyStaffFilters);
        departmentFilter?.addEventListener("change", applyStaffFilters);
        staffSearchInput?.addEventListener("input", applyStaffFilters);
        applyStaffFilters();
    }

    const staffAudioButtons = document.querySelectorAll("[data-staff-audio-button]");

    if (staffAudioButtons.length > 0) {
        const staffAudioPlayer = new Audio();
        let activeAudioButton = null;

        const resetActiveAudioButton = () => {
            if (activeAudioButton) {
                activeAudioButton.classList.remove("is-playing");
                activeAudioButton.setAttribute("aria-pressed", "false");
            }

            activeAudioButton = null;
        };

        staffAudioButtons.forEach((button) => {
            button.setAttribute("aria-pressed", "false");

            button.addEventListener("click", () => {
                const audioSource = button.dataset.audioSrc;

                if (!audioSource) {
                    return;
                }

                if (activeAudioButton === button && !staffAudioPlayer.paused) {
                    staffAudioPlayer.pause();
                    resetActiveAudioButton();
                    return;
                }

                resetActiveAudioButton();
                activeAudioButton = button;
                staffAudioPlayer.src = audioSource;
                button.classList.add("is-playing");
                button.setAttribute("aria-pressed", "true");

                staffAudioPlayer.play().catch(resetActiveAudioButton);
            });
        });

        staffAudioPlayer.addEventListener("ended", resetActiveAudioButton);
        staffAudioPlayer.addEventListener("pause", () => {
            if (staffAudioPlayer.ended) {
                resetActiveAudioButton();
            }
        });
    }

    const researchSwitcher = document.querySelector(".research-switcher");
    const researchSearchInput = document.querySelector("[data-research-search]");
    const researchItems = document.querySelectorAll("[data-research-item]");
    const researchPanels = document.querySelectorAll("[data-research-panel]");
    const researchEmptyText = document.querySelector("[data-research-empty]");

    if (researchSwitcher && researchSearchInput && researchItems.length > 0) {
        const applyResearchSearch = () => {
            const searchQuery = researchSearchInput.value.trim().toLowerCase();
            const hasSearch = searchQuery !== "";
            let totalVisibleItems = 0;

            researchSwitcher.classList.toggle("is-searching", hasSearch);

            researchItems.forEach((item) => {
                const searchText = item.dataset.search || item.textContent.toLowerCase();
                const isVisible = !hasSearch || searchText.includes(searchQuery);

                item.hidden = !isVisible;

                if (isVisible) {
                    totalVisibleItems += 1;
                }
            });

            researchPanels.forEach((panel) => {
                if (!hasSearch) {
                    panel.hidden = false;
                    return;
                }

                const visibleItems = panel.querySelectorAll("[data-research-item]:not([hidden])");
                panel.hidden = visibleItems.length === 0;
            });

            if (researchEmptyText) {
                researchEmptyText.hidden = !hasSearch || totalVisibleItems > 0;
            }
        };

        researchSearchInput.addEventListener("input", applyResearchSearch);
        applyResearchSearch();
    }

    const activitySlider = document.querySelector("[data-activity-slider]");
    const activitySlides = document.querySelectorAll("[data-activity-slide]");
    const activityCounter = document.querySelector("[data-activity-counter]");

    if (activitySlider && activitySlides.length > 1) {
        let currentSlideIndex = 0;

        const showActivitySlide = (targetIndex) => {
            activitySlides.forEach((slide, index) => {
                slide.classList.toggle("is-active", index === targetIndex);
            });

            if (activityCounter) {
                activityCounter.textContent = `${targetIndex + 1} / ${activitySlides.length}`;
            }
        };

        window.setInterval(() => {
            currentSlideIndex = (currentSlideIndex + 1) % activitySlides.length;
            showActivitySlide(currentSlideIndex);
        }, 4000);
    }

});
