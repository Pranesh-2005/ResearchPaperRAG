const API_BASE = "https://researchpaperragbackend.onrender.com";
let chatHistory = [];
let sessionId = null;

async function uploadPDF() {
  const fileInput = document.getElementById("pdfInput");
  if (!fileInput.files.length) {
    alert("Select a PDF first!");
    return;
  }
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  document.getElementById("status").innerText = "Uploading...";

  const res = await fetch(API_BASE + "/upload", { method: "POST", body: formData });
  const data = await res.json();
  if (res.ok) {
    sessionId = data.session_id;
    chatHistory = data.chat_history || [];
    document.getElementById("status").innerText = "Upload successful!";
    renderChat();
  } else {
    document.getElementById("status").innerText = "Error: " + data.error;
  }
}

async function ask() {
  const msg = document.getElementById("message").value;
  if (!msg) return;
  const res = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: msg,
      chat_history: chatHistory
    })
  });
  const data = await res.json();
  if (res.ok) {
    chatHistory = data.chat_history;
    renderChat();
    document.getElementById("message").value = "";
  } else {
    alert("Error: " + data.error);
  }
}

async function clearChat() {
  const res = await fetch(`${API_BASE}/clear`, { method: "POST" });
  const data = await res.json();
  if (res.ok) {
    chatHistory = [];
    renderChat();
  }
}

function renderChat() {
  const chatBox = document.getElementById("chat");
  chatBox.innerHTML = "";
  chatHistory.forEach(([user, bot]) => {
    if (user) {
      const row = document.createElement("div");
      row.className = "msg user-row";

      const label = document.createElement("div");
      label.className = "label user";
      label.textContent = "You";

      const bubble = document.createElement("div");
      bubble.className = "bubble user";
      bubble.textContent = user;

      row.appendChild(label);
      row.appendChild(bubble);
      chatBox.appendChild(row);
    }
    if (bot) {
      const row = document.createElement("div");
      row.className = "msg bot-row";

      const label = document.createElement("div");
      label.className = "label bot";
      label.textContent = "Bot";

      const bubble = document.createElement("div");
      bubble.className = "bubble bot markdown";
      try {
        bubble.innerHTML = window.marked.parse(bot);
      } catch (e) {
        bubble.textContent = bot;
      }

      row.appendChild(label);
      row.appendChild(bubble);
      chatBox.appendChild(row);
    }
  });
  chatBox.scrollTop = chatBox.scrollHeight;
}