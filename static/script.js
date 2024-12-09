let conversationHistory = [];
let isSending = false;

document.getElementById('chat-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;

    if (message.trim() === '' || isSending) return;

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div class="user-message">${message}</div>`;

    conversationHistory.push({ role: 'user', content: message });

    const sendButton = document.getElementById('send-button');
    sendButton.disabled = true;
    isSending = true;

    const response = await fetch('/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(conversationHistory)
    });

    const assistantResponse = await response.json();
    conversationHistory.push({ role: 'assistant', content: assistantResponse });
    chatBox.innerHTML += `<div class="assistant-message">${assistantResponse}</div>`;
    messageInput.value = '';
    sendButton.disabled = false;
    isSending = false;
});

document.getElementById('clear-button').addEventListener('click', function () {
    const messageInput = document.getElementById('message-input');
    messageInput.value = '';
});
