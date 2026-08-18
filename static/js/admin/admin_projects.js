// Main purpose: drive the dynamic project-management form behavior in the admin interface.
// Program logic note.
// Program logic note.
// Program logic note.
// Program logic note.
// Program logic note.

document.addEventListener("DOMContentLoaded", () => {
    const projectTypeSelect = document.querySelector("[data-project-type]");
    const projectScopedSections = document.querySelectorAll("[data-project-scope]");
    const projectRequiredFields = document.querySelectorAll("[data-project-required]");
    const researcherList = document.querySelector("[data-researcher-list]");
    const engineerList = document.querySelector("[data-engineer-list]");
    const assistantList = document.querySelector("[data-assistant-list]");
    const teamList = document.querySelector("[data-custom-team-list]");
    const detailList = document.querySelector("[data-custom-detail-list]");

    const addResearcherButton = document.querySelector("[data-add-researcher]");
    const addEngineerButton = document.querySelector("[data-add-engineer]");
    const addAssistantButton = document.querySelector("[data-add-assistant]");
    const addTeamButton = document.querySelector("[data-add-custom-team]");
    const addDetailButton = document.querySelector("[data-add-custom-detail]");

    function syncRequiredIndicators() {
        projectRequiredFields.forEach((field) => {
            const label = document.querySelector(`label[for='${field.id}']`);
            const indicator = label?.querySelector("[data-required-indicator]");

            if (indicator) {
                indicator.hidden = !field.required;
            }
        });
    }

    function toggleProjectFields() {
        // Program logic note.
        const projectType = projectTypeSelect?.value === "finished" ? "finished" : "ongoing";

        projectScopedSections.forEach((section) => {
            const isVisible = section.dataset.projectScope === projectType;
            section.hidden = !isVisible;
        });

        projectRequiredFields.forEach((field) => {
            const requirement = field.dataset.projectRequired;
            field.required =
                requirement === "always" ||
                (requirement === "ongoing" && projectType === "ongoing") ||
                (requirement === "finished" && projectType === "finished");
        });

        syncRequiredIndicators();
    }

    // Program logic note.
    // Program logic note.
    function createTextField({ name, value = "", placeholder = "", rows = 3, type = "textarea" }) {
        if (type === "input") {
            const input = document.createElement("input");
            input.type = "text";
            input.name = name;
            input.value = value;
            input.placeholder = placeholder;
            return input;
        }

        const textarea = document.createElement("textarea");
        textarea.name = name;
        textarea.rows = rows;
        textarea.placeholder = placeholder;
        textarea.value = value;
        return textarea;
    }

    // Program logic note.
    // Program logic note.
    function parseJsonScript(scriptId) {
        try {
            return JSON.parse(document.getElementById(scriptId)?.textContent || "[]");
        } catch (error) {
            return [];
        }
    }

    // Program logic note.
    function syncDynamicSectionState(listElement, buttonElement) {
        if (!listElement || !buttonElement) {
            return;
        }

        const hasItems = listElement.children.length > 0;

        if (hasItems) {
            listElement.removeAttribute("hidden");
            buttonElement.classList.add("is-expanded");
            buttonElement.textContent = buttonElement.dataset.expandedLabel || buttonElement.textContent;
        } else {
            listElement.setAttribute("hidden", "");
            buttonElement.classList.remove("is-expanded");
            buttonElement.textContent = buttonElement.dataset.collapsedLabel || buttonElement.textContent;
        }
    }

    // Program logic note.
    function openDynamicSection(listElement, buttonElement) {
        listElement?.removeAttribute("hidden");
        syncDynamicSectionState(listElement, buttonElement);
    }

    // Program logic note.
    // Program logic note.
    function createRemoveButton() {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "link-button";
        button.textContent = "Delete This Field";
        button.addEventListener("click", () => {
            const card = button.closest(".admin-dynamic-card");
            const list = card?.parentElement;
            card?.remove();

            if (list === researcherList) {
                syncDynamicSectionState(researcherList, addResearcherButton);
            } else if (list === engineerList) {
                syncDynamicSectionState(engineerList, addEngineerButton);
            } else if (list === assistantList) {
                syncDynamicSectionState(assistantList, addAssistantButton);
            } else if (list === teamList) {
                syncDynamicSectionState(teamList, addTeamButton);
            } else if (list === detailList) {
                syncDynamicSectionState(detailList, addDetailButton);
            }
        });
        return button;
    }

    // Program logic note.
    function createExistingPhotoPreview(filename, altText) {
        const preview = document.createElement("div");
        preview.className = "admin-upload-preview";

        const currentPhoto = document.createElement("p");
        currentPhoto.className = "admin-current-file";
        currentPhoto.textContent = `Current photo: ${filename}`;

        const media = document.createElement("div");
        media.className = "admin-upload-preview-media admin-upload-preview-media-image";

        const image = document.createElement("img");
        image.src = `/static/uploads/${filename}`;
        image.alt = altText;

        media.appendChild(image);
        preview.append(currentPhoto, media);
        return preview;
    }

    // Program logic note.
    function createPhotoUploadField({ inputName, label, filename = "", altText = "" }) {
        const photoWrap = document.createElement("div");
        photoWrap.className = "admin-form-grid";

        const photoLabel = document.createElement("label");
        photoLabel.textContent = label;
        photoWrap.appendChild(photoLabel);

        const uploadField = document.createElement("div");
        uploadField.className = "admin-upload-field";
        uploadField.setAttribute("data-upload-field", "");

        if (filename) {
            uploadField.appendChild(createExistingPhotoPreview(filename, altText || `${label} preview`));
        }

        const selectedPreview = document.createElement("div");
        selectedPreview.className = "admin-upload-preview admin-upload-preview-selected";
        selectedPreview.setAttribute("data-selected-preview", "");
        selectedPreview.hidden = true;

        const photoInput = document.createElement("input");
        photoInput.type = "file";
        photoInput.name = inputName;
        photoInput.accept = ".jpg,.jpeg,.png,.gif,.webp,image/*";
        photoInput.setAttribute("data-file-preview", "image");

        uploadField.append(photoInput, selectedPreview);
        photoWrap.appendChild(uploadField);

        window.AdminFilePreviews?.enhanceInput(photoInput);

        return photoWrap;
    }

    // Program logic note.
    function renderProjectMemberField(field = {}, config = {}) {
        const card = document.createElement("div");
        card.className = "admin-dynamic-card";

        const actions = document.createElement("div");
        actions.className = "admin-dynamic-actions";
        actions.appendChild(createRemoveButton());

        const grid = document.createElement("div");
        grid.className = "admin-form-grid admin-form-grid-two";

        const nameEnWrap = document.createElement("div");
        const nameEnLabel = document.createElement("label");
        nameEnLabel.textContent = `${config.memberTitle} Name EN`;
        nameEnWrap.appendChild(nameEnLabel);
        nameEnWrap.appendChild(createTextField({
            name: `${config.fieldPrefix}_name_en[]`,
            value: field.name_en || "",
            placeholder: "ex. Dr. Example Name",
            type: "input",
        }));

        const nameThWrap = document.createElement("div");
        const nameThLabel = document.createElement("label");
        nameThLabel.textContent = `${config.memberTitle} Name TH`;
        nameThWrap.appendChild(nameThLabel);
        nameThWrap.appendChild(createTextField({
            name: `${config.fieldPrefix}_name_th[]`,
            value: field.name_th || "",
            placeholder: "e.g. Thai researcher name",
            type: "input",
        }));

        grid.append(nameEnWrap, nameThWrap);

        const hiddenPhoto = document.createElement("input");
        hiddenPhoto.type = "hidden";
        hiddenPhoto.name = `${config.fieldPrefix}_existing_photo[]`;
        hiddenPhoto.value = field.photo_filename || "";

        const photoWrap = createPhotoUploadField({
            inputName: `${config.fieldPrefix}_photo_file[]`,
            label: `${config.memberTitle} Photo`,
            filename: field.photo_filename || "",
            altText: `${field.name_en || config.memberTitle} current photo`,
        });
        photoWrap.insertBefore(hiddenPhoto, photoWrap.children[1] || null);

        const photoHint = document.createElement("p");
        photoHint.className = "admin-form-hint";
        photoHint.textContent = "Optional. Upload only if this person's photo is not already available in the staff list.";
        photoWrap.appendChild(photoHint);

        card.append(actions, grid, photoWrap);
        config.listElement?.appendChild(card);
    }

    // Program logic note.
    function renderCustomTeamField(field = {}) {
        // Program logic note.
        const card = document.createElement("div");
        card.className = "admin-dynamic-card";

        const actions = document.createElement("div");
        actions.className = "admin-dynamic-actions";
        actions.appendChild(createRemoveButton());

        const grid = document.createElement("div");
        grid.className = "admin-form-grid admin-form-grid-two";

        const labelEnWrap = document.createElement("div");
        const labelEn = document.createElement("label");
        labelEn.textContent = "Field Label EN";
        labelEnWrap.appendChild(labelEn);
        labelEnWrap.appendChild(createTextField({
            name: "custom_team_label_en[]",
            value: field.label_en || "",
            placeholder: "ex. Project Liaison",
            type: "input",
        }));

        const labelThWrap = document.createElement("div");
        const labelTh = document.createElement("label");
        labelTh.textContent = "Field Label TH";
        labelThWrap.appendChild(labelTh);
        labelThWrap.appendChild(createTextField({
            name: "custom_team_label_th[]",
            value: field.label_th || "",
            placeholder: "e.g. Field Coordinator in Thai",
            type: "input",
        }));

        const valueEnWrap = document.createElement("div");
        const valueEn = document.createElement("label");
        valueEn.textContent = "Person Name EN";
        valueEnWrap.appendChild(valueEn);
        valueEnWrap.appendChild(createTextField({
            name: "custom_team_value_en[]",
            value: field.value_en || "",
            placeholder: "ex. Dr. Example Name",
            type: "input",
        }));

        const valueThWrap = document.createElement("div");
        const valueTh = document.createElement("label");
        valueTh.textContent = "Person Name TH";
        valueThWrap.appendChild(valueTh);
        valueThWrap.appendChild(createTextField({
            name: "custom_team_value_th[]",
            value: field.value_th || "",
            placeholder: "e.g. Thai team member name",
            type: "input",
        }));

        grid.append(labelEnWrap, labelThWrap, valueEnWrap, valueThWrap);

        const hiddenPhoto = document.createElement("input");
        hiddenPhoto.type = "hidden";
        hiddenPhoto.name = "custom_team_existing_photo[]";
        hiddenPhoto.value = field.photo_filename || "";

        const photoWrap = createPhotoUploadField({
            inputName: "custom_team_photo_file[]",
            label: "Photo",
            filename: field.photo_filename || "",
            altText: `${field.value_en || "Custom team"} current photo`,
        });
        photoWrap.insertBefore(hiddenPhoto, photoWrap.children[1] || null);

        const photoHint = document.createElement("p");
        photoHint.className = "admin-form-hint";
        photoHint.textContent = "Optional. Upload only if this person's photo is not already available in the staff list.";
        photoWrap.appendChild(photoHint);

        card.append(actions, grid, photoWrap);
        teamList?.appendChild(card);
    }

    // Program logic note.
    function renderCustomDetailField(field = {}) {
        // Program logic note.
        const card = document.createElement("div");
        card.className = "admin-dynamic-card";

        const actions = document.createElement("div");
        actions.className = "admin-dynamic-actions";
        actions.appendChild(createRemoveButton());

        const grid = document.createElement("div");
        grid.className = "admin-form-grid admin-form-grid-two";

        const labelEnWrap = document.createElement("div");
        const labelEn = document.createElement("label");
        labelEn.textContent = "Field Label EN";
        labelEnWrap.appendChild(labelEn);
        labelEnWrap.appendChild(createTextField({
            name: "custom_detail_label_en[]",
            value: field.label_en || "",
            placeholder: "ex. Project Website",
            type: "input",
        }));

        const labelThWrap = document.createElement("div");
        const labelTh = document.createElement("label");
        labelTh.textContent = "Field Label TH";
        labelThWrap.appendChild(labelTh);
        labelThWrap.appendChild(createTextField({
            name: "custom_detail_label_th[]",
            value: field.label_th || "",
            placeholder: "e.g. Project Website in Thai",
            type: "input",
        }));

        const valueEnWrap = document.createElement("div");
        const valueEn = document.createElement("label");
        valueEn.textContent = "Content EN";
        valueEnWrap.appendChild(valueEn);
        valueEnWrap.appendChild(createTextField({
            name: "custom_detail_value_en[]",
            value: field.value_en || "",
            placeholder: "ex. https://example.com",
            rows: 4,
        }));

        const valueThWrap = document.createElement("div");
        const valueTh = document.createElement("label");
        valueTh.textContent = "Content TH";
        valueThWrap.appendChild(valueTh);
        valueThWrap.appendChild(createTextField({
            name: "custom_detail_value_th[]",
            value: field.value_th || "",
            placeholder: "ex. https://example.com",
            rows: 4,
        }));

        grid.append(labelEnWrap, labelThWrap, valueEnWrap, valueThWrap);

        card.append(actions, grid);
        detailList?.appendChild(card);
    }

    // Program logic note.
    const memberSections = [
        {
            listElement: researcherList,
            buttonElement: addResearcherButton,
            initialData: parseJsonScript("researcher-fields-data"),
            fieldPrefix: "researcher",
            memberTitle: "Researcher",
        },
        {
            listElement: engineerList,
            buttonElement: addEngineerButton,
            initialData: parseJsonScript("engineer-fields-data"),
            fieldPrefix: "engineer",
            memberTitle: "Engineer",
        },
        {
            listElement: assistantList,
            buttonElement: addAssistantButton,
            initialData: parseJsonScript("assistant-fields-data"),
            fieldPrefix: "assistant",
            memberTitle: "Assistant",
        },
    ];

    memberSections.forEach((section) => {
        section.buttonElement?.addEventListener("click", () => {
            openDynamicSection(section.listElement, section.buttonElement);
            renderProjectMemberField({}, section);
            syncDynamicSectionState(section.listElement, section.buttonElement);
        });

        if (section.initialData.length) {
            section.initialData.forEach((field) => renderProjectMemberField(field, section));
            openDynamicSection(section.listElement, section.buttonElement);
        } else {
            syncDynamicSectionState(section.listElement, section.buttonElement);
        }
    });

    const customSections = [
        {
            listElement: teamList,
            buttonElement: addTeamButton,
            initialData: parseJsonScript("custom-team-fields-data"),
            renderField: renderCustomTeamField,
        },
        {
            listElement: detailList,
            buttonElement: addDetailButton,
            initialData: parseJsonScript("custom-detail-fields-data"),
            renderField: renderCustomDetailField,
        },
    ];

    customSections.forEach((section) => {
        section.buttonElement?.addEventListener("click", () => {
            openDynamicSection(section.listElement, section.buttonElement);
            section.renderField({});
            syncDynamicSectionState(section.listElement, section.buttonElement);
        });

        if (section.initialData.length) {
            section.initialData.forEach(section.renderField);
            openDynamicSection(section.listElement, section.buttonElement);
        } else {
            syncDynamicSectionState(section.listElement, section.buttonElement);
        }
    });

    projectTypeSelect?.addEventListener("change", toggleProjectFields);
    toggleProjectFields();
});

