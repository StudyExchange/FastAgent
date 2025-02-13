let currentAPI = '/lightrag/';
let conversationHistory = [];
let isSending = false;
document.getElementById('lightrag-api-btn').classList.add('active');

document.getElementById('chat-api-btn').addEventListener('click', function() {
    currentAPI = '/chat/';
    document.getElementById('chat-api-btn').classList.add('active');
    document.getElementById('react-api-btn').classList.remove('active');
    document.getElementById('lightrag-api-btn').classList.remove('active');
    conversationHistory = [];
    document.getElementById('chat-box').innerHTML = '';
});

document.getElementById('react-api-btn').addEventListener('click', function() {
    currentAPI = '/react/';
    document.getElementById('react-api-btn').classList.add('active');
    document.getElementById('chat-api-btn').classList.remove('active');
    document.getElementById('lightrag-api-btn').classList.remove('active');
    conversationHistory = [];
    document.getElementById('chat-box').innerHTML = '';
});

document.getElementById('lightrag-api-btn').addEventListener('click', function() {
    currentAPI = '/lightrag/';
    document.getElementById('lightrag-api-btn').classList.add('active');
    document.getElementById('chat-api-btn').classList.remove('active');
    document.getElementById('react-api-btn').classList.remove('active');
    conversationHistory = [];
    document.getElementById('chat-box').innerHTML = '';
});

document.getElementById('chat-form').addEventListener('submit', async function(event) {
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
    const response = await fetch(currentAPI, {
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

document.getElementById('clear-button').addEventListener('click', function() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
    conversationHistory = [];
    const messageInput = document.getElementById('message-input');
    messageInput.value = '';
});