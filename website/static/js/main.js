function openchat(){
    var btn = document.getElementById("chat");
    var chatbox = document.getElementById("chatbox");
    document.getElementById(chatbox.classList.remove('visually-hidden'));
}

function closechat(){
    var btn = document.getElementById("close");
    var chatbox = document.getElementById("chatbox");
    document.getElementById(chatbox.classList.add('visually-hidden'));
}