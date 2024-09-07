document.getElementById('send-btn').addEventListener('click', function() {
    let userInput = document.getElementById('user-input').value.trim();

    if (userInput !== "") {
        appendMessage(userInput, 'user-message');
        document.getElementById('user-input').value = '';

        // Input ve butonu devre dışı bırak
        toggleInputState(true);

        // "Mesaj oluşturuluyor..." animasyonunu göster
        if (!document.querySelector('.typing-indicator')) {  // Eğer daha önce eklenmemişse
            let typingIndicator = createTypingIndicator();
            document.getElementById('chat-box').appendChild(typingIndicator);
            scrollToBottom();
        }

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => response.json())
        .then(data => {
            let typingIndicator = document.querySelector('.typing-indicator');
            if (typingIndicator) typingIndicator.remove(); // Animasyonu kaldır
            appendMessage(data.response, 'bot-message');

            // Sadece ilk mesaj değilse beğenme ve beğenmeme butonlarını ekle
            if (data.response !== "Merhaba! Size nasıl yardımcı olabilirim?") {
                addFeedbackButtons();
            }

            // Input ve butonu yeniden etkinleştir
            toggleInputState(false);
        })
        .catch(error => {
            console.error('Error:', error);
            let typingIndicator = document.querySelector('.typing-indicator');
            if (typingIndicator) typingIndicator.remove(); // Animasyonu kaldır

            // Input ve butonu yeniden etkinleştir
            toggleInputState(false);

            // Hata durumunda kullanıcıya bir mesaj göster
            appendMessage('Bir hata oluştu. Lütfen tekrar deneyin.', 'bot-message');
        });
    }
});

function toggleInputState(disable) {
    document.getElementById('user-input').disabled = disable;
    document.getElementById('send-btn').disabled = disable;
}

function createTypingIndicator(noBorder = false) {
    let typingIndicator = document.createElement('div');
    typingIndicator.className = 'message typing-indicator';
    
    if (noBorder) {
        typingIndicator.style.border = 'none';  // Beyaz çerçeveyi kaldır
    }
    
    let typingText = document.createElement('span');
    typingText.className = 'typing-indicator-text';
    typingText.textContent = 'Mesaj oluşturuluyor...';

    typingIndicator.appendChild(typingText);
    
    return typingIndicator;
}

function addFeedbackButtons() {
    let chatBox = document.getElementById('chat-box');
    let feedbackContainer = document.createElement('div');
    feedbackContainer.className = 'feedback-buttons';

    let likeButton = document.createElement('button');
    likeButton.className = 'feedback-btn like-btn';
    likeButton.innerHTML = '<i class="fas fa-thumbs-up"></i>'; // Thumbs-up ikonu

    let dislikeButton = document.createElement('button');
    dislikeButton.className = 'feedback-btn dislike-btn';
    dislikeButton.innerHTML = '<i class="fas fa-thumbs-down"></i>'; // Thumbs-down ikonu

    let speakButton = document.createElement('button');
    speakButton.className = 'feedback-btn speak-btn';
    speakButton.innerHTML = '<i class="fas fa-volume-up"></i>'; // Sesli okuma ikonu

    let regenerateButton = document.createElement('button');
    regenerateButton.className = 'feedback-btn regenerate-btn';
    regenerateButton.innerHTML = '<i class="fas fa-redo"></i>'; // Yeniden oluşturma ikonu

    feedbackContainer.appendChild(likeButton);
    feedbackContainer.appendChild(dislikeButton);
    feedbackContainer.appendChild(speakButton);
    feedbackContainer.appendChild(regenerateButton);

    chatBox.appendChild(feedbackContainer);

    likeButton.addEventListener('click', function() {
        alert("Yanıtı beğendiniz!");
    });

    dislikeButton.addEventListener('click', function() {
        const userMessageElement = feedbackContainer.previousElementSibling.previousElementSibling;
        const botMessageElement = feedbackContainer.previousElementSibling;
    
        const userMessage = userMessageElement ? userMessageElement.textContent.trim() : '';
        const botMessage = botMessageElement ? botMessageElement.textContent.trim() : '';
    
        fetch('/save-feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_message: userMessage,
                bot_message: botMessage
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert("Geri bildiriminiz kaydedildi.");
            } else {
                alert("Geri bildirim kaydedilemedi: " + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Bir hata oluştu. Geri bildirim kaydedilemedi.");
        });
    });
    

    speakButton.addEventListener('click', function() {
        const botMessageElement = feedbackContainer.previousElementSibling;
        const botMessage = botMessageElement ? botMessageElement.textContent.trim() : '';
        const speech = new SpeechSynthesisUtterance(botMessage);
        window.speechSynthesis.speak(speech);
    });

    regenerateButton.addEventListener('click', function() {
        const userMessageElement = feedbackContainer.previousElementSibling.previousElementSibling;
        const userMessage = userMessageElement ? userMessageElement.textContent.trim() : '';

        const botMessageElement = feedbackContainer.previousElementSibling;

        // Mevcut bot mesajını temizleyip, animasyonu ekle
        botMessageElement.innerHTML = ''; // Mevcut mesajı temizle
        let typingIndicator = createTypingIndicator(true);  // Çerçevesiz animasyon
        botMessageElement.appendChild(typingIndicator);

        // Çerçevenin hemen kalkmasını sağla
        setTimeout(() => {
            botMessageElement.style.border = 'none';
        }, 0);

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Yeni yanıtı mevcut bot mesajının yerine koy ve çerçeveyi geri ekleme
            botMessageElement.classList.remove('typing-indicator');
            botMessageElement.style.border = 'none';  // Beyaz çerçeveyi geri eklemeyin
            botMessageElement.textContent = data.response;
        })
        .catch(error => {
            console.error('Error:', error);
            botMessageElement.textContent = 'Bir hata oluştu. Lütfen tekrar deneyin.';
        });
    });
}

function appendMessage(message, className) {
    let chatBox = document.getElementById('chat-box');
    let messageElement = document.createElement('div');
    messageElement.className = `message ${className}`;
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    scrollToBottom();
}

function scrollToBottom() {
    let chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}
