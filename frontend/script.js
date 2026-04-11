function send() {
  let msg = document.getElementById("msg").value;
  if (!msg) return;

  let chatbox = document.getElementById("chatbox");

  // User message
  chatbox.innerHTML += `<div class="message user">${msg}</div>`;

  document.getElementById("msg").value = "";

  // Typing animation
  let typing = document.createElement("div");
  typing.className = "message bot";
  typing.innerText = "Typing...";
  chatbox.appendChild(typing);

  chatbox.scrollTop = chatbox.scrollHeight;

  fetch("https://chatbot-project-htzx.onrender.com/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ message: msg })
  })
  .then(res => res.json())
  .then(data => {
    typing.remove();

    chatbox.innerHTML += `<div class="message bot">${data.response}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;
  });
}

// Enter key support
document.getElementById("msg").addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    send();
  }
});