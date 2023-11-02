const chatBtn = document.querySelector('button[name="chatbtn"]');


chatBtn.addEventListener('click', e=>{
    var currentURL = window.location.href;
    console.log(currentURL);
    var match = currentURL.split('together_detail')[1];
    match = match.match(/\d+/);
    console.log(match);
    const h2Element = document.querySelector('.blog_details h2');
    console.log(h2Element);
    var title = h2Element.textContent;


    if (match) {
        var room_name = match[0];
        const resp = fetch('/check_room/'+ room_name +'/' + title)
        .then(resp => resp.json())
        .then(data => console.log(data))
    } else {
        console.log("숫자를 찾을 수 없습니다.");
    }
})

// {% for chat_room in chat_room_list %}
//                 <div class="friend" id="room_{{chat_room.room_name}}" >
//                     <img src=""/>
//                     <p>
//                         <strong>room_{{chat_room.room_name}}</strong>
//                         <span>{{chat_room.last_message}}</span>
//                     </p>
//                     <p class='lastmessage'>{{chat_room.last_message}}</p>
//                     <div class="status available">
//                     </div>
//                 </div>
//             {% endfor %}