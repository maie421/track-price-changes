/**
 *  open ai
 *  https://platform.openai.com/docs/api-reference/making-requests
 */
const chatMessages = document.querySelector('#chat-messages');
const userInput = document.querySelector('#user-input input');
const sendButton = document.querySelector('#user-input button');
const apiKey = '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';
const apiEndpoint = 'https://api.openai.com/v1/chat/completions'
function addMessage(content, isUser) {
  var chatMessages = document.getElementById('chat-messages');

  var messageContainer = document.createElement('div');
  messageContainer.classList.add('d-flex', 'flex-row', 'justify-content-' + (isUser ? 'end' : 'start'), 'mb-4');

  var messageDiv = document.createElement('div');
  messageDiv.classList.add('p-3', isUser ? 'me-3' : 'ms-3', 'border','rounded-3');
  messageDiv.classList.add(isUser ? 'bg-light' : 'bg-info');

  var messageParagraph = document.createElement('p');
  messageParagraph.classList.add('small', 'mb-0');
  messageParagraph.textContent = content;

  messageDiv.appendChild(messageParagraph);
  messageContainer.appendChild(messageDiv);

  // 새로운 메시지를 가장 아래에 추가
  chatMessages.insertBefore(messageContainer, chatMessages.firstChild);
  // 스크롤을 가장 아래로 이동
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addProductElement(productData) {
    let chatMessages = document.getElementById('chat-messages');
    let newDiv = document.createElement('div');
    newDiv.className = 'd-flex mb-4';
    newDiv.style.width = '50px';
    newDiv.style.marginLeft = '19px';

    let discount_rate = Math.round(productData.discount_rate);
    let increase_rate = Math.round(productData.increase_rate);

    newDiv.innerHTML = `
        <div class="col mb-3">
            <a href="/product?pid=${productData.product_id}">
                <div class="card h-100">
                    <img class="card-img-top" src="${productData.image}" alt="${productData.name}">
                    <div class="card-body p-4">
                        <div class="text-center">
                            <h5 class="fw-bolder two-line-text">${productData.name}</h5>
                            ${discount_rate > 0 ? `<span class="discount-box" style="background-color: red;">▼ ${discount_rate}%</span>` : ''}
                            ${increase_rate > 0 ? `<span class="discount-box" style="background-color: #14AF40;">▲ ${increase_rate}%</span>` : ''}
                            ${productData.price}원
                        </div>
                    </div>
                </div>
            </a>
        </div>
    `;

    chatMessages.insertBefore(newDiv, chatMessages.firstChild);
    chatMessages.scrollTop = chatMessages.scrollHeight;
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

async function fetchProductResponse(prompt) {
    const requestOptions = {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        },
    };
    try {
        const response = await fetch(`/v1/search?keyword=${prompt}`, requestOptions);
        return await response.json();
    } catch (error) {
        console.error(error)
        return 'api 상품 오류';
    }
}

sendButton.addEventListener('click', async () => {
    const message = userInput.value.trim();
    if (message.length === 0) return;
    addMessage(message, true);
    userInput.value = '';

    const aiResponse = await fetchAIResponse(message);
    addMessage(aiResponse, false);

    const productResponse = await fetchProductResponse(message);
    let productData = productResponse['products']['0'];
    if (productData !== undefined)
        addProductElement(productData);
});
// userInput.addEventListener('keydown', (event) => {
//     if (event.key === 'Enter') {
//         sendButton.click();
//     }
// });

document.getElementById('open-chat').addEventListener('click', function() {
   var chatContainer = document.getElementById('chat-container');
   chatContainer.style.visibility = chatContainer.style.visibility === 'visible' ? 'hidden' : 'visible';
});