function addComment(){
    const input = document.querySelector('input[name="comment_input"]');
    let value = input.value;
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    var data = {
        'content':value,
    }

    let resp = fetch('/board/add_comment/'+postPk.{
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,  // CSRF 토큰 설정
        },
        body:JSON.stringify(data),
    })
    .then(resp => resp.json())
    .then(data =>{
        console.log(data)
    })
}
