let currentAPI = '/react/';
let conversationHistory = [];
let isSending = false;

// API切换按钮事件
document.getElementById('chat-api-btn').addEventListener('click', function() {
    currentAPI = '/chat/';
    // 切换active类
    document.getElementById('chat-api-btn').classList.add('active');
    document.getElementById('react-api-btn').classList.remove('active');
    // 清空对话历史和聊天框
    conversationHistory = [];
    document.getElementById('chat-box').innerHTML = '';
});

document.getElementById('react-api-btn').addEventListener('click', function() {
    currentAPI = '/react/';
    // 切换active类
    document.getElementById('react-api-btn').classList.add('active');
    document.getElementById('chat-api-btn').classList.remove('active');
    // 清空对话历史和聊天框
    conversationHistory = [];
    document.getElementById('chat-box').innerHTML = '';
});

// 发送消息事件
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

// 清空聊天记录按钮事件
document.getElementById('clear-button').addEventListener('click', function () {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
    conversationHistory = [];
    const messageInput = document.getElementById('message-input');
    messageInput.value = '';
});