var chatCloseBtn = document.querySelector(".close-box");
var chatBox = document.querySelector("#chatbox");
var chatOpenBtn = document.querySelector(".open-box");
var backArrow = document.querySelector(".back-arrow");

chatCloseBtn.addEventListener('click', e=>{
    
    chatBox.style.display = "none";
    chatOpenBtn.style.display = "flex";
    chatCloseBtn.style.display = "none";

})

chatOpenBtn.addEventListener('click', e=>{
    chatBox.style.display = "block";
    chatOpenBtn.style.display = "none";
    chatCloseBtn.style.display = "flex";
    let friends = document.querySelector("#friends-box");
    const csrftoken = getSessionId();

    const resp = fetch('/room_list', {
        method: 'GET',
        headers: {
            'Authorization': `Token ${csrftoken}`,
            'Content-Type': 'application/json',
        },
    })
    .then(resp => resp.json())
    .then(data => {
        let html = '';
        friends.innerHTML = '';
        
        for (let i=0; i < data.length; i++ ){
            console.log(data[i]);
            let html = `
            <div class="friend-content" id="room_${data[i].room_name}" onclick="linkChatRoom(event)">
                <img src=""/>
                <p>
                    <strong>room_${data[i].room_title}</strong>
                    <span>${data[i].last_message   }</span>
                </p>
                <p class='lastmessage'>${data[i].last_message}</p>
                <div class="status available">
                </div>
            </div>
            `;
            friends.innerHTML += html;

        }
        });
    })
    


// csrf 토큰 얻어오기
function getSessionId() {
    // 쿠키 문자열 가져오기
    const cookies = document.cookie.split(';');

    // 세션 아이디 찾기
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            // 'sessionid=' 다음의 문자열이 세션 아이디입니다.
            return cookie.substring('sessionid='.length);
        }
    }

    // 세션 아이디가 없을 경우 null 또는 원하는 기본값을 반환할 수 있습니다.
    return null;
}


function linkChatRoom (e){

    console.log(e.currentTarget);
    const roomName = e.currentTarget.id.split('_')[1];
    let friendList = document.querySelector("#friendslist");
    friendList.style.display ='hidden';
    let chatview = document.querySelector("#chatview");
    chatview.style.display = 'block';
    const rtwindow = document.getElementById("chat-messages");
    const input = document.querySelector("#sendmessage input");
    rtwindow.style.opacity = 1;
    rtwindow.innerHTML = '';
    const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomName + '/');
    console.log(chatSocket);
    const scroll = function (div){
        div.scrollTop = div.scrollHeight;
    }
    chatSocket.onmessage = (e=>{
        const data = JSON.parse(e.data);
        if (data.username != username){
            let messageHtml = `
            <div class="message">
                <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/1_copy.jpg"/>
                    <div class="bubble">
                    ${data.message}
                        <div class="corner"></div>
                    </div>
                </div>
            `;
            console.log(messageHtml);
            rtwindow.innerHTML += messageHtml;
        }
        else{
            let sendHtml = `
            <div class="message right">
                <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/2_copy.jpg"/>
                    <div class="bubble">
                    ${data.message}
                        <div class="corner"></div>
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
    let backArrow = document.querySelector(".back-arrow");
    backArrow.addEventListener('click',e=>{
        gobackArrow(e);
    })
    function gobackArrow(e){
        chatSocket.close();
        friendList.style.display ='block';
        chatview.style.display = 'none';
    }

}