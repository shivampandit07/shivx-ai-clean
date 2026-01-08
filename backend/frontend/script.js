async function send() {
  const input = document.getElementById("msg");
  const msg = input.value.trim();
  if (!msg) return;

  const chat = document.getElementById("chat");

  chat.innerHTML += `<p><b>You:</b> ${msg}</p>`;
  input.value = "";

  chat.innerHTML += `<p><i>ShivX is typing...</i></p>`;
  chat.scrollTop = chat.scrollHeight;

  try {
    const res = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    chat.lastChild.innerHTML = `<b>ShivX:</b> ${data.reply}`;
  } catch (err) {
    chat.lastChild.innerHTML = `<b>Error:</b> Backend not responding`;
  }

  chat.scrollTop = chat.scrollHeight;
}
