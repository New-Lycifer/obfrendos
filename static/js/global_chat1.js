function loadMessages() {
    fetch('/global_chat/') // Отправляем GET-запрос на сервер
        .then(response => response.json()) // Преобразуем полученный ответ в формат JSON
        .then(data => {
            // Обновляем содержимое чата на странице
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML = ''; // Очищаем содержимое чата перед добавлением новых сообщений
            data.messages.forEach(msg => {
                const messageElement = document.createElement('p');
                messageElement.innerHTML = `<strong>${msg.author}:</strong> ${msg.content} <em>${msg.created_at}</em>`;
                chatBox.appendChild(messageElement);
            });
        })
        .catch(error => {
            console.error('Ошибка при загрузке сообщений чата:', error);
        });
}

// Вызываем функцию для загрузки сообщений чата при загрузке страницы
window.addEventListener('load', loadMessages);

// Функция для отправки сообщения чата
function sendMessage() {
    const messageInput = document.getElementById('message-input').value;
    if (messageInput.trim() === '') {
        return; // Не отправляем пустые сообщения
    }

    fetch('/global_chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Получаем CSRF-токен для безопасной отправки POST-запроса
        },
        body: JSON.stringify({ message: messageInput }) // Преобразуем данные в формат JSON и отправляем на сервер
    })
    .then(() => {
        // После успешной отправки сообщения обновляем список сообщений
        loadMessages();
        // Очищаем поле ввода сообщения
        document.getElementById('message-input').value = '';
    })
    .catch(error => {
        console.error('Ошибка при отправке сообщения чата:', error);
    });
}

// Функция для получения CSRF-токена из cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Обработчик события для отправки сообщения при нажатии на Enter в поле ввода
document.getElementById('message-input').addEventListener('keypress', event => {
    if (event.key === 'Enter') {
        event.preventDefault(); // Предотвращаем стандартное поведение (перенос строки)
        sendMessage(); // Отправляем сообщение
    }
});