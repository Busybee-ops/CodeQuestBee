document.addEventListener("DOMContentLoaded", function () {
    // Handle dynamic tab loading
    window.loadTab = function(url, clickedElement, event) {
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

                // Update session variable for last accessed tab
                fetch('/update_last_tab', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ last_tab: clickedElement.dataset.url.replace('/', '') })
                });
            })
            .catch(error => console.error("Error loading content:", error));
    };

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

     // Function to reset the form and clear the result
     window.resetForm = function() {
        const form = document.getElementsByTagName('form')[0];
        if (form) { 
            form.reset();
        }
        const result = document.getElementById("main-content");
        if (result) {
            result.innerHTML = '';
        }
    };
});

// Function to update the content area (maintains a uniform structure)
function updateMainContent(data) {
    const mainContent = document.getElementById("main-content");

    // Create a temporary DOM element to parse the response
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = data;

    // Extract the content from the response
    const newContentElement = tempDiv.querySelector('#main-content');
    const newContent = newContentElement ? newContentElement.innerHTML : data;

    // Clear current content in #main-content
    mainContent.innerHTML = newContent;
}