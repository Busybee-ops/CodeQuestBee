document.addEventListener("DOMContentLoaded", function () {
    // Handle dynamic tab loading
    function loadTab(url, clickedElement, event) {
        if (event) {
            event.preventDefault();
        }
        history.pushState(null, "", url);

        fetch(url)
            .then(response => response.text())
            .then(data => {
                updateMainContent(data); // Inject new content
                // Reattach the form handlers to any newly loaded forms
                attachFormHandler();

                // Update active tab
                document.querySelectorAll(".nav-link").forEach(link => link.classList.remove("active"));
                if (clickedElement) {
                    clickedElement.classList.add("active");
                }
            })
            .catch(error => console.error("Error loading content:", error));
    }

    // Attach click event to all navigation links to handle tab loading
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function (event) {
            loadTab(this.dataset.url, this, event);
        });
    });

    // Attach the form handler to all forms on the page
    function attachFormHandler() {
        // Attach form handlers for all forms
        document.querySelectorAll("form").forEach(form => {
            form.addEventListener("submit", function (event) {
                event.preventDefault(); // Prevent full page reload

                const formData = new FormData(form);
                const url = form.action;

                fetch(url, {
                    method: "POST",
                    body: formData
                })
                .then(response => response.text())
                .then(data => {
                    updateMainContent(data); // Inject form submission result into main content
                    // No need to call attachFormHandler again here since it's already done after content is loaded
                })
                .catch(error => console.error("Error submitting form:", error));
            });
        });
    }

    // Ensure that form handlers are attached on page load
    attachFormHandler();

    // Handle browser back/forward button (history state changes)
    window.onpopstate = function () {
        loadTab(window.location.pathname, document.querySelector(".nav-link[data-url='" + window.location.pathname + "']"));
    };
});

// Function to update the content area (maintains a uniform structure)
function updateMainContent(data) {
    const mainContent = document.getElementById("main-content");

    // Clear current content in #main-content
    mainContent.innerHTML = ''; 

    // Create a div to hold the new content
    const resultDiv = document.createElement('div');
    resultDiv.classList.add('result'); // Add a class for styling

    // Insert new content (form result, etc.)
    resultDiv.innerHTML = data;

    // Append the new content to #main-content
    mainContent.appendChild(resultDiv);
}