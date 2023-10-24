function changeWindow (e) {
    const chatWindow = document.getElementById("chat-window");
    chatWindow.style.display = 'block';
    const html = `
        <div class="rtwindow">
        </div>
        <div class="input-box">
            <input type='text>
        </div>
    `;
    chatWindow.innerHTML += html;

    const roomName = e.id.split("_")[1];
    console.log(roomName);

    const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomName + '/')

    chatSocket.onmessage(e=>{
        const data = JSON.parse(e.data);
        const messageHtml = `
            <div class='message-box'>
                <div class='other-message'>
                    ${data}
                </div>
            </div>
        `;
        const rtwindow = document.getElementsByClassName("rtwindow");
        rtwindow.innerHTML += messageHtml;
    })
}