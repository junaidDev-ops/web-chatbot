const input = document.getElementById("msg-input");
const chatBox = document.getElementById("chat-box");

async function sendMessage() {
    const msg = input.value;
    input.value = "";

    
    chatBox.innerHTML += `<div class="user-msg">${msg}</div>`;

    
    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg})
    });

    const data = await res.json();

    
    chatBox.innerHTML += `<div class="ai-msg">${data.reply}</div>`;
}