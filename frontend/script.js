const user = localStorage.getItem("user");
if (!user) {
  window.location.href = "login.html";
}
document.addEventListener("DOMContentLoaded", () => {

  const chatbox = document.getElementById("chatbox");
  const input = document.getElementById("msg");
  const button = document.querySelector("button");

  /* Send message */
  function send() {
    const msg = input.value.trim();
    if (!msg) return;

    addMessage(msg, "user");
    input.value = "";

    showTyping();

    fetch("https://chatbot-project-htzx.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    })
      .then(res => res.json())
      .then(data => {
        removeTyping();
        addMessage(data.response || "No response 🤔", "bot");
      })
      .catch(() => {
        removeTyping();
        addMessage("Server error ❌", "bot");
      });
  }

  /* Add message */
  function addMessage(text, type) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", type);

    const img = document.createElement("img");
    img.src = type === "user"
      ? "https://cdn-icons-png.flaticon.com/512/847/847969.png"
      : "https://cdn-icons-png.flaticon.com/512/4712/4712109.png";

    const span = document.createElement("span");
    span.textContent = text;

    msgDiv.appendChild(img);
    msgDiv.appendChild(span);

    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  /* Typing indicator */
  function showTyping() {
    const typing = document.createElement("div");
    typing.classList.add("message", "bot");
    typing.id = "typing";

    typing.innerHTML = `
      <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"/>
      <span>Typing...</span>
    `;

    chatbox.appendChild(typing);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  function removeTyping() {
    const t = document.getElementById("typing");
    if (t) t.remove();
  }

  /* Enter key */
  input.addEventListener("keypress", e => {
    if (e.key === "Enter") send();
  });

  /* Button click */
  button.addEventListener("click", send);

});