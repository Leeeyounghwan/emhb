document.addEventListener("DOMContentLoaded", function(){

})


function changeWindow (e) {
    const chatWindow = document.getElementById("chat-window");
    const chatList = document.getElementById('chat-list');
    const input = document.getElementById('chat-input');
    const rtwindow = document.getElementsByClassName("rt-window")[0];
    const back = document.getElementsByClassName("back")[0];
    chatList.style.display = 'none';
    chatWindow.style.display = 'flex';

    rtwindow.innerHTML = '';
    const roomName = e.currentTarget.id.split('_')[1];

    const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomName + '/')

    const scroll = function (div){
        div.scrollTop = div.scrollHeight;
    }
    chatSocket.onmessage = (e=>{
        const data = JSON.parse(e.data);
        if (data.username != username){
            let messageHtml = `
            <div class='other-message-box'>
                <div class='user-name'>
                    ${data.username}
                </div>
                <div class='other-message'>
                    ${data.message}
                </div>
            </div>
            `;
            rtwindow.innerHTML += messageHtml;
        }
        else{
            let sendHtml = `
            <div class='your-message-box'>
                <div class='user-name'>
                    ${data.username}
                </div>
                <div class='your-message'>
                    ${data.message}
                </div>
            </div>
            `;
            rtwindow.innerHTML += sendHtml;
        }
        scroll(rtwindow);
    })

    input.focus()
    input.onkeyup = function(e){
        if (e.key === 'Enter'){
            let mydata = input.value;
            chatSocket.send(JSON.stringify({
                'username': username,
                'message': mydata
            }));
            input.value = '';
        }
    }
    back.addEventListener("click", e=>{
        chatWindow.style.display ='none';
        chatList.style.display = 'flex'
        chatSocket.close();
    })
}