const chatbotmodal = document.getElementById("chatbot-modal");
const openModalBtn = document.getElementById("open-modal");
const closeModalBtn = document.getElementById("close-modal");
const closeBox = document.getElementById("close-box");
const modalInput = document.querySelector(".modal-input");
const contentDiv = document.querySelector(".modal-content");

//스크롤 최신채팅으로
let scroll = function (div) {
    div.scrollTop = div.scrollHeight;
}

// 모달창 열기
openModalBtn.addEventListener("click", () => {
    chatbotmodal.style.display = "flex";
    openModalBtn.style.display = 'none';
    //   document.body.style.overflow = "hidden"; // 스크롤바 제거
    closeBox.style.display = 'flex';
});

// 모달창 닫기
closeBox.addEventListener("click", () => {
    chatbotmodal.style.display = "none";
    document.body.style.overflow = "auto"; // 스크롤바 보이기
    closeBox.style.display = 'none';
    openModalBtn.style.display = 'flex';
});

console.log(modalInput);
modalInput.addEventListener('keyup', e => {
    if (e.keyCode === 13) {
        const question = modalInput.value;
        modalInput.value = ''
        console.log(question);

        let qHtml = `
            <div class='question-box'>
                <div class='question'>
                    ${question}
                </div>
            </div>
        `;
        contentDiv.innerHTML += (qHtml);
        scroll(contentDiv);

        let answerBox = document.createElement('div');
        answerBox.className = 'answer-box';

        let answer = document.createElement('div');
        answer.className = 'answer';

        let loading = document.createElement('div');


        answerBox.append(loading);
        contentDiv.append(answerBox);
        loading.id = 'loading';
        loading.className = 'answer';
        scroll(contentDiv);

        const resp = fetch('chatapi/' + question).then(
            resp => {
                return resp.json()
            }
        )
            .then(data => {

                loading.remove();
                answer.innerText = data['answer'];
                answerBox.append(answer);
                scroll(contentDiv);
            }

            )
            .catch(error => {
                console.error("error: ", error);
                loading.remove();
            })
    }
})