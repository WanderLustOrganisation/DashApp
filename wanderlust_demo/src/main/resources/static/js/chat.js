document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('messageInput').addEventListener('keypress', () => {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
    
    document.getElementById('sendButton').addEventListener('click', function() {
        sendMessage();
    });
    
    
    const socket = new WebSocket("ws://localhost:8080/chat");
    
    socket.onopen = function(event){
        console.log('Connected to the server');
    }
    
    socket.onmessage = function(event){
        addMessage(event.text, event.type, event.username)
    }
    
    function sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        console.log(message)
    
        socket.send(message)
        input.value = '';
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
    
});