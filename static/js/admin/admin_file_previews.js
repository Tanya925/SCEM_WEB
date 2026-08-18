// Main purpose: provide instant image, audio, and document previews for admin upload fields.

(function () {
    function clearPreview(previewElement) {
        if (!previewElement) {
            return;
        }

        const objectUrl = previewElement.dataset.objectUrl;
        if (objectUrl) {
            URL.revokeObjectURL(objectUrl);
            delete previewElement.dataset.objectUrl;
        }

        previewElement.innerHTML = "";
        previewElement.hidden = true;
    }

    function renderPreview(previewElement, previewType, file) {
        clearPreview(previewElement);

        if (!previewElement || !file) {
            return;
        }

        const objectUrl = URL.createObjectURL(file);
        previewElement.dataset.objectUrl = objectUrl;
        previewElement.hidden = false;

        const selectedLabel = document.createElement("p");
        selectedLabel.className = "admin-current-file";
        selectedLabel.textContent = `Selected file: ${file.name}`;
        previewElement.appendChild(selectedLabel);

        const media = document.createElement("div");
        media.className = "admin-upload-preview-media";

        if (previewType === "image") {
            media.classList.add("admin-upload-preview-media-image");
            const image = document.createElement("img");
            image.src = objectUrl;
            image.alt = file.name;
            media.appendChild(image);
        } else if (previewType === "audio") {
            media.classList.add("admin-upload-preview-media-audio");
            const audio = document.createElement("audio");
            audio.controls = true;
            audio.preload = "metadata";
            const source = document.createElement("source");
            source.src = objectUrl;
            if (file.type) {
                source.type = file.type;
            }
            audio.appendChild(source);
            audio.append("Your browser does not support audio preview.");
            media.appendChild(audio);
        } else if (previewType === "pdf") {
            media.classList.add("admin-upload-preview-media-document");
            const iframe = document.createElement("iframe");
            iframe.src = objectUrl;
            iframe.title = file.name;

            media.appendChild(iframe);
        }

        previewElement.appendChild(media);
    }

    function enhanceInput(inputElement) {
        if (!inputElement || inputElement.dataset.previewReady === "true") {
            return;
        }

        const previewType = inputElement.dataset.filePreview;
        if (!previewType) {
            return;
        }

        const field = inputElement.closest("[data-upload-field]");
        const previewElement = field?.querySelector("[data-selected-preview]");

        inputElement.addEventListener("change", () => {
            const file = inputElement.files && inputElement.files[0];
            if (!file) {
                clearPreview(previewElement);
                return;
            }

            renderPreview(previewElement, previewType, file);
        });

        inputElement.dataset.previewReady = "true";
    }

    function init(root = document) {
        root.querySelectorAll("[data-file-preview]").forEach((inputElement) => {
            enhanceInput(inputElement);
        });
    }

    window.AdminFilePreviews = {
        clearPreview,
        enhanceInput,
        init,
    };

    document.addEventListener("DOMContentLoaded", () => {
        init(document);
    });
})();
