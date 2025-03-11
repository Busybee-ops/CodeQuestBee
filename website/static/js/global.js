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

                // Execute any script tags in the loaded content
                executeScripts(data);

                // Manually load the ttt.js script if the Tic-Tac-Toe page is loaded
                if (url.includes('/tictactoe/')) {
                    loadScript('/static/js/ttt.js', function() {
                        if (typeof initializeGame === 'function') {
                            initializeGame();
                        } else {
                            console.error("initializeGame function is not defined.");
                        }
                    });
                }
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
                .then(response => response.json())
                .then(data => {
                    // Display the result
                    const resultDiv = document.getElementById('result');
                    if (resultDiv) {
                        resultDiv.innerHTML = generateResultHTML(data);
                    }
                    // Reset the form
                    form.reset();
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
        const result = document.getElementById("result");
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

// Function to execute script tags in the loaded content
function executeScripts(data) {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = data;
    const scripts = tempDiv.querySelectorAll('script');
    scripts.forEach(script => {
        if (script.src) {
            // Check if the script is already added
            if (!document.querySelector(`script[src="${script.src}"]`)) {
                const newScript = document.createElement('script');
                newScript.type = script.type || 'text/javascript';
                newScript.src = script.src;
                document.head.appendChild(newScript);
            }
        } else {
            // Check if the inline script is already added
            const inlineScriptExists = Array.from(document.querySelectorAll('script'))
                .some(existingScript => existingScript.textContent === script.textContent);
            if (!inlineScriptExists) {
                const newScript = document.createElement('script');
                newScript.type = script.type || 'text/javascript';
                newScript.textContent = script.textContent;
                document.head.appendChild(newScript);
            }
        }
    });
}

// Function to load a script dynamically
function loadScript(src, callback) {
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = src;
    script.onload = callback;
    document.head.appendChild(script);
}

// Function to generate the result HTML based on the data
function generateResultHTML(data) {
    console.log(data);
    if (data.liters && data.ounces && data.bottles) {
        return `
            <div class="card text-white bg-success mb-3" style="max-width: 60rem;">
                <div class="card-header">Here you go</div>
                <div class="card-body">
                    <h4 class="card-title"></h4>
                    <p class="card-text">Recommended Water Intake: ${data.liters.toFixed(2)} Liters or ${data.ounces.toFixed(2)} Ounces or ${data.bottles} Bottles</p>
                </div>
            </div>
        `;
    } else if (data.weather && data.temperature) {
        return `
           <div class="card text-white bg-success mb-3" style="max-width: 60rem;">
                <div class="card-header">Weather Information</div>
                <div class="card-body">
                    <h4 class="card-title"></h4>
                    <p class="card-text">Weather: ${data.weather}, Temperature: ${data.temperature}°F</p>
                </div>
            </div>
        `;

    } else if (data.name && data.email && data.message) {
        return `
        <div class="card text-white bg-success mb-3" style="max-width: 60rem;">
        <div class="card-header">Contact</div>
        <div class="card-body">
            <h4 class="card-title"></h4>
            <p class="card-text">Thank you for contacting us, ${data.name}. We will get back to you soon!</p>
        </div>
    </div>
        `;
    }
    else if (data.error) {
        return `<p class="text-danger">${data.error}</p>`;
    } else {
        return `<p class="text-danger">Unexpected result format.</p>`;
    }
}