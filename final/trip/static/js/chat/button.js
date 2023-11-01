var chatCloseBtn = document.querySelector(".close-box");
var chatBox = document.querySelector("#chatbox");
var chatOpenBtn = document.querySelector(".open-box");

chatCloseBtn.addEventListener('click', e=>{
    
    chatBox.style.display = "none";
    chatOpenBtn.style.display = "flex";
    chatCloseBtn.style.display = "none";

})

chatOpenBtn.addEventListener('click', e=>{
    chatBox.style.display = "block";
    chatOpenBtn.style.display = "none";
    chatCloseBtn.style.display = "flex";
    let friends = document.querySelector("#friends");
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
        <div class="friend" id="room_${data[i].room_name}" >
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

// 세션 아이디 가져와서 출력 또는 다른 용도로 사용