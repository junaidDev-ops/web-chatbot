const input = document.getElementById("msg-input");
const chatBox = document.getElementById("chat-box");
const sidebar = document.getElementById("sidebar");
const menuBtn = document.getElementById("menu-btn");

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

menuBtn.addEventListener("click", function() {
    sidebar.style.left = "0px";
});

document.addEventListener("click", function(event) {
    if (!sidebar.contains(event.target) && !menuBtn.contains(event.target)) {
        sidebar.style.left = "-250px";
    }
});