/**
 *  open ai
 *  https://platform.openai.com/docs/api-reference/making-requests
 */
const chatMessages = document.querySelector('#chat-messages');
const userInput = document.querySelector('#user-input input');
const sendButton = document.querySelector('#user-input button');
const apiKey = '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';
const apiEndpoint = 'https://api.openai.com/v1/chat/completions'
function addMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message';
    messageElement.textContent = `${sender}: ${message}`;
    chatMessages.prepend(messageElement);
}

async function fetchAIResponse(prompt) {
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model: "ft:gpt-3.5-turbo-0613:personal::8aZbTg6m",
            messages: [{
                role: "user",
                content: prompt
            }, ],
            temperature: 0.8,
            max_tokens: 1024,
            top_p: 1,
            frequency_penalty: 0.5,
            presence_penalty: 0.5,
            stop: ["Human"],
        }),
    };
    // API 요청후 응답 처리
    try {
        const response = await fetch(apiEndpoint, requestOptions);
        const data = await response.json();
        const aiResponse = data.choices[0].message.content;
        return aiResponse;
    } catch (error) {
		console.error('OpenAI API 호출 중 오류 발생:', error);
        return 'OpenAI API 호출 중 오류 발생';
    }
}

sendButton.addEventListener('click', async () => {
    console.log("테스트");
    const message = userInput.value.trim();
    if (message.length === 0) return;
    addMessage('나', message);
    userInput.value = '';
    const aiResponse = await fetchAIResponse(message);
    addMessage('챗봇', aiResponse);
});
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        console.log("테스트");
        sendButton.click();
    }
});

document.getElementById('open-chat').addEventListener('click', function() {
   var chatContainer = document.getElementById('chat-container');
   chatContainer.style.visibility = chatContainer.style.visibility === 'visible' ? 'hidden' : 'visible';
});