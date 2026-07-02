function addMessage(text, type) {
    const chatBox = document.getElementById("chatBox");

    const msg = document.createElement("div");
    msg.classList.add(type === "user" ? "user-msg" : "bot-msg");
    msg.innerText = text;

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 🧠 typing indicator
function showTyping() {
    const chatBox = document.getElementById("chatBox");

    const typing = document.createElement("div");
    typing.classList.add("typing");
    typing.id = "typing";
    typing.innerText = "Zenith is thinking...";

    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
}

async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();

    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    showTyping();

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await response.json();

    removeTyping();
    addMessage(data.reply, "bot");
}
async function getReport() {
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "summary" })
    });

    const data = await response.json();
    addMessage("📊 Session Report Requested", "user");
    addMessage(data.reply, "bot");
}