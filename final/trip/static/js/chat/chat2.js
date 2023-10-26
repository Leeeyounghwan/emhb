$(document).ready(function(){
  
    var preloadbg = document.createElement("img");
    preloadbg.src = "https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/timeline1.png";
    
    $("#searchfield").focus(function(){
      if($(this).val() == "Search contacts..."){
        $(this).val("");
      }
    });
    $("#searchfield").focusout(function(){
      if($(this).val() == ""){
        $(this).val("Search contacts...");
        
      }
    });
    
    $("#sendmessage input").focus(function(){
      if($(this).val() == "Send message..."){
        $(this).val("");
      }
    });
    $("#sendmessage input").focusout(function(){
      if($(this).val() == ""){
        $(this).val("Send message...");
        
      }
    });
      
    
    $(".friend").each(function(){   
      $(this).click(function(){
        var childOffset = $(this).offset();
        var parentOffset = $(this).parent().parent().offset();
        var childTop = childOffset.top - parentOffset.top;
        var clone = $(this).find('img').eq(0).clone();
        var top = childTop+12+"px";
        
        $(clone).css({'top': top}).addClass("floatingImg").appendTo("#chatbox");                  
        
        setTimeout(function(){$("#profile p").addClass("animate");$("#profile").addClass("animate");}, 100);
        setTimeout(function(){
          $("#chat-messages").addClass("animate");
          $('.cx, .cy').addClass('s1');
          setTimeout(function(){$('.cx, .cy').addClass('s2');}, 100);
          setTimeout(function(){$('.cx, .cy').addClass('s3');}, 200);     
        }, 150);                            
        
        $('.floatingImg').animate({
          'width': "68px",
          'left':'108px',
          'top':'20px'
        }, 200);
        
        var name = $(this).find("p strong").html();
        var email = $(this).find("p span").html();                            
        $("#profile p").html(name);
        $("#profile span").html(email);     
        
        $(".message").not(".right").find("img").attr("src", $(clone).attr("src"));                  
        $('#friendslist').fadeOut();
        $('#chatview').fadeIn();
        
        const roomName = $(this).attr('id').split('_')[1];
        const rtwindow = document.getElementById("chat-messages");
        const input = document.querySelector("#sendmessage input");

        const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomName + '/')
    
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
        
        $('#close').unbind("click").click(function(){       
          $("#chat-messages, #profile, #profile p").removeClass("animate");
          $('.cx, .cy').removeClass("s1 s2 s3");
          $('.floatingImg').animate({
            'width': "40px",
            'top':top,
            'left': '12px'
          }, 200, function(){$('.floatingImg').remove()});        
          
          setTimeout(function(){
            $('#chatview').fadeOut();
            $('#friendslist').fadeIn();       
          }, 50);
          chatSocket.close();
        });
        
      });
    });     
  });

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
            <div class="message">
                <img src=""/>
                    ${data.username}
                  <div class="bubble">
                    ${data.message}
                      <div class="corner"></div>
                  </div>
              </div>
            `;
            rtwindow.innerHTML += messageHtml;
        }
        else{
            let sendHtml = `
            <div class="message right">
                <img src=""/>
                    ${data.username}
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
    back.addEventListener("click", e=>{
        chatWindow.style.display ='none';
        chatList.style.display = 'flex'
        chatSocket.close();
    })
}