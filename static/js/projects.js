document.addEventListener(
    "DOMContentLoaded",
    function () {

        const searchInput =
            document.getElementById(
                "project-search"
            );

        const statusFilter =
            document.getElementById(
                "project-status"
            );

        const skillFilter =
            document.getElementById(
                "project-skill"
            );

        const sortSelect =
            document.getElementById(
                "projectSort"
            );

        const filterForm =
            document.getElementById(
                "projectFilterForm"
            );

        const projectGrid =
            document.querySelector(
                ".projects-grid"
            );

        const projectItems =
            document.querySelectorAll(
                ".project-item"
            );

        const noProjectsFound =
            document.getElementById(
                "noProjectsFound"
            );

        const projectCount =
            document.getElementById(
                "projectCount"
            );

        // ==========================================
        // SAFETY CHECK
        // ==========================================

        if (
            !searchInput ||
            !statusFilter ||
            !skillFilter ||
            !sortSelect ||
            !projectGrid ||
            !noProjectsFound
        ) {

            console.log(
                "Project elements not found."
            );

            return;

        }

        console.log(
            "Projects JS loaded successfully."
        );

        // ==========================================
        // FILTER PROJECTS
        // ==========================================

        function filterProjects() {

            const searchText =
                searchInput.value
                    .toLowerCase()
                    .trim();

            const selectedStatus =
                statusFilter.value;

            const selectedSkill =
                skillFilter.value;

            let visibleProjects = 0;

            projectItems.forEach(
                function (project) {

                    const projectName =
                        project.dataset.projectName
                            .toLowerCase();

                    const projectStatus =
                        project.dataset.projectStatus;

                    const projectSkill =
                        project.dataset.projectSkill;

                    // SEARCH MATCH

                    const matchesSearch =
                        projectName.includes(
                            searchText
                        );

                    // STATUS MATCH

                    const matchesStatus =
                        selectedStatus === "" ||
                        projectStatus ===
                            selectedStatus;

                    // SKILL MATCH

                    const matchesSkill =
                        selectedSkill === "" ||
                        projectSkill ===
                            selectedSkill;

                    // FINAL MATCH

                    if (
                        matchesSearch &&
                        matchesStatus &&
                        matchesSkill
                    ) {

                        project.classList.remove(
                            "d-none"
                        );

                        visibleProjects++;

                    } else {

                        project.classList.add(
                            "d-none"
                        );

                    }

                }
            );

            // ======================================
            // NO RESULT MESSAGE
            // ======================================

            if (
                visibleProjects === 0 &&
                projectItems.length > 0
            ) {

                noProjectsFound.classList.remove(
                    "d-none"
                );

            } else {

                noProjectsFound.classList.add(
                    "d-none"
                );

            }

            // ======================================
            // PROJECT COUNT
            // ======================================

            if (projectCount) {

                projectCount.textContent =
                    visibleProjects;

            }

        }

        // ==========================================
        // SORT PROJECTS
        // ==========================================

        function sortProjects() {

            const sortValue =
                sortSelect.value;

            const projects =
                Array.from(
                    projectItems
                );

            projects.sort(
                function (a, b) {

                    // ==============================
                    // NAME A → Z
                    // ==============================

                    if (
                        sortValue === "name_asc"
                    ) {

                        return a.dataset.projectName
                            .localeCompare(
                                b.dataset.projectName
                            );

                    }

                    // ==============================
                    // NAME Z → A
                    // ==============================

                    if (
                        sortValue === "name_desc"
                    ) {

                        return b.dataset.projectName
                            .localeCompare(
                                a.dataset.projectName
                            );

                    }

                    // ==============================
                    // PROGRESS HIGH → LOW
                    // ==============================

                    if (
                        sortValue === "progress_high"
                    ) {

                        return Number(
                            b.dataset.projectProgress
                        ) - Number(
                            a.dataset.projectProgress
                        );

                    }

                    // ==============================
                    // PROGRESS LOW → HIGH
                    // ==============================

                    if (
                        sortValue === "progress_low"
                    ) {

                        return Number(
                            a.dataset.projectProgress
                        ) - Number(
                            b.dataset.projectProgress
                        );

                    }

                    // ==============================
                    // OLDEST UPDATED
                    // ==============================

                    if (
                        sortValue === "oldest"
                    ) {

                        return Number(
                            a.dataset.projectUpdated
                        ) - Number(
                            b.dataset.projectUpdated
                        );

                    }

                    // ==============================
                    // NEWEST UPDATED
                    // ==============================

                    return Number(
                        b.dataset.projectUpdated
                    ) - Number(
                        a.dataset.projectUpdated
                    );

                }
            );

            // ======================================
            // PUT SORTED PROJECTS BACK
            // ======================================

            projects.forEach(
                function (project) {

                    projectGrid.appendChild(
                        project
                    );

                }
            );

        }

        // ==========================================
        // LIVE SEARCH
        // ==========================================

        searchInput.addEventListener(
            "input",
            filterProjects
        );


        // ==========================================
        // STATUS FILTER
        // ==========================================

        statusFilter.addEventListener(
            "change",
            filterProjects
        );


        // ==========================================
        // SKILL FILTER
        // ==========================================

        skillFilter.addEventListener(
            "change",
            filterProjects
        );

        // ==========================================
        // SORT
        // ==========================================

        sortSelect.addEventListener(
            "change",
            function () {

                sortProjects();

                filterProjects();

            }
        );

        // ==========================================
        // SEARCH FORM
        // ==========================================

        if (filterForm) {

            filterForm.addEventListener(
                "submit",
                function (event) {

                    event.preventDefault();

                    filterProjects();

                }
            );

        }

        sortProjects();

        filterProjects();

    }
);