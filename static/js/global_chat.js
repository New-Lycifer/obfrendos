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
        .then(response => response.json())
        .then(data => {
            // Append the new message to the chat
            var chatBox = document.getElementById("chat-box");
            var newMessage = document.createElement("div");
            newMessage.classList.add("message");
            newMessage.innerHTML = `<em>${data.created_at}</em><p><strong><a href="/profile/${data.author_id}/">${data.author}</a></strong>: ${data.content}</p>`;
            chatBox.appendChild(newMessage);
            document.getElementById("message-input").value = ""; // Clear the input field
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
        })
        .catch(error => console.error('Error:', error));
    });