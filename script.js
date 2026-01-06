function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    // Adăugăm mesajul utilizatorului (dreapta)
    addMessage(message, 'user');
    input.value = '';
    input.focus();

    // Trimitem la server
    fetch(`/chat/?query=${encodeURIComponent(message)}`)
        .then(response => {
            if (!response.ok) throw new Error('Eroare server');
            return response.json();
        })
        .then(data => {
            // Adăugăm răspunsul principal (stânga)
            addMessage(data.response, 'bot');

            // Adăugăm produsele (stânga)
            if (data.detalii && data.detalii.length > 0) {
                data.detalii.forEach(item => {
                    addMessage(item, 'bot', 'product');
                });
            }
        })
        .catch(error => {
            console.error('Eroare:', error);
            addMessage("Eroare de comunicare. Încearcă din nou.", 'bot', 'error');
        });
}

function addMessage(text, sender, type = '') {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');

    msgDiv.className = `message ${sender}-message ${type}`;

    // Adăugăm iconiță pentru mesajele de produs
    if (type === 'product') {
        const icon = document.createElement('i');
        icon.className = 'fas fa-shoe-prints'; // sau altă iconiță relevantă
        msgDiv.appendChild(icon);
    }

    // Adăugăm textul
    const textNode = document.createTextNode(text);
    msgDiv.appendChild(textNode);

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Ascultăm pentru tasta Enter
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});