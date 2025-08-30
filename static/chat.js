const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');

// Focus on input when page loads
messageInput.focus();

// Send message when Enter is pressed
messageInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input and disable send button
    messageInput.value = '';
    sendButton.disabled = true;
    sendButton.textContent = 'Sending...';
    
    // Show typing indicator
    showTypingIndicator();

    // Send message to backend
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.success) {
            // Use smooth typewriter effect for all responses
            addTypewriterMessage(data.response, 'bot');
        } else {
            addMessage(data.error || 'Sorry, there was an error processing your message.', 'bot', true);
        }
    })
    .catch(error => {
        removeTypingIndicator();
        addMessage('Sorry, there was a connection error. Please try again.', 'bot', true);
        console.error('Error:', error);
    })
    .finally(() => {
        // Re-enable send button
        sendButton.disabled = false;
        sendButton.textContent = 'Send';
        messageInput.focus();
    });
}

function addMessage(text, sender, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = text;
    
    if (isError) {
        messageContent.style.color = '#d32f2f';
    }
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypewriterMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content typewriter-container';
    
    // Add cursor element
    const cursor = document.createElement('span');
    cursor.className = 'typewriter-cursor';
    cursor.textContent = '|';
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Start typewriter effect with word-by-word animation
    const words = text.split(' ');
    let currentText = '';
    let wordIndex = 0;
    
    function typeWord() {
        if (wordIndex < words.length) {
            currentText += (wordIndex > 0 ? ' ' : '') + words[wordIndex];
            messageContent.innerHTML = currentText + '<span class="typewriter-cursor">|</span>';
            
            wordIndex++;
            
            // Scroll to bottom as text appears
            chatMessages.scrollTo({
                top: chatMessages.scrollHeight,
                behavior: 'smooth'
            });
            
            // Variable speed based on word length and punctuation
            let delay = 100; // base delay
            const currentWord = words[wordIndex - 1];
            
            // Longer pause after punctuation
            if (currentWord && (currentWord.includes('.') || currentWord.includes('!') || currentWord.includes('?'))) {
                delay = 400;
            } else if (currentWord && currentWord.includes(',')) {
                delay = 200;
            } else if (currentWord && currentWord.length > 8) {
                delay = 150; // Slightly longer for long words
            }
            
            setTimeout(typeWord, delay);
        } else {
            // Remove cursor when done
            setTimeout(() => {
                messageContent.innerHTML = currentText;
            }, 1000);
        }
    }
    
    typeWord();
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.id = 'typing-indicator';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const typingDots = document.createElement('div');
    typingDots.className = 'typing-dots';
    typingDots.innerHTML = '<span></span><span></span><span></span>';
    
    messageContent.appendChild(typingDots);
    typingDiv.appendChild(messageContent);
    chatMessages.appendChild(typingDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}