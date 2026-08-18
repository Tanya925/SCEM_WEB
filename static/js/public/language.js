// Main purpose: mark the active public-site language button based on body[data-language].

document.addEventListener("DOMContentLoaded", () => {
    const currentLanguage = document.body.dataset.language;
    const languageButtons = document.querySelectorAll("[data-lang-button]");

    languageButtons.forEach((button) => {
        if (button.dataset.lang === currentLanguage) {
            button.classList.add("is-active");
        } else {
            button.classList.remove("is-active");
        }
    });
});
