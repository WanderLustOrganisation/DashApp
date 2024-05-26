document.getElementById('messageInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

document.getElementById('sendButton').addEventListener('click', function() {
    sendMessage();
});

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (message) {
        addMessage(message, 'user');
        input.value = '';
        // Aquí podrías agregar lógica para enviar el mensaje a otros usuarios
        // Simularemos un mensaje de otro usuario
        setTimeout(() => {
            addMessage('Mensaje de otro usuario', 'other', 'Usuario123');
        }, 1000);
    }
}

function addMessage(text, type, username) {
    const messagesContainer = document.getElementById('messages');
    
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message-container', type);

    const messageElement = document.createElement('div');
    messageElement.classList.add('message', type);

    const messageText = document.createElement('span');
    messageText.textContent = text;
    messageElement.appendChild(messageText);

    if (type === 'other') {
        const meta = document.createElement('div');
        meta.classList.add('meta');
        const now = new Date();
        const timestamp = now.toLocaleString();
        meta.textContent = `${username} - ${timestamp}`;
        messageElement.appendChild(meta);
    }

    messageContainer.appendChild(messageElement);
    messagesContainer.appendChild(messageContainer);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
