document.getElementById("message-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        var formData = new FormData(this);

        // Get CSRF token
        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Send form data via AJAX
        fetch(this.action, {
            method: this.method,
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Add header to identify AJAX request
                'X-CSRFToken': csrftoken // Add CSRF token
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update chat messages on the page
            var chatBox = document.getElementById("chat-box");
            chatBox.innerHTML = data.html; // Update the HTML content
            document.getElementById("message-input").value = ""; // Clear the input field
        })
        .catch(error => console.error('Error:', error));
    });