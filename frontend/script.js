function send(){
fetch("https://chatbot.onrender.com/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:msg.value})
})
.then(r=>r.json())
.then(d=>res.innerText=d.response);
}