const trigger = document.getElementById("ai-chat-trigger");
const overlay = document.getElementById("ai-chat-overlay");
const closeBtn = document.getElementById("ai-chat-close");
const input = document.getElementById("ai-chat-input");
const askBtn = document.getElementById("ai-chat-ask");
const messages = document.getElementById("ai-chat-messages");
const urlParams = new URLSearchParams(window.location.search);
const cardId = urlParams.get("id");

trigger.addEventListener("click", () => {
    overlay.classList.add("active");
    document.body.classList.add("no-overflow");
});
closeBtn.addEventListener("click", closeChat);
overlay.addEventListener("click", (e) => {if (e.target === overlay) closeChat();});

function closeChat() {
    overlay.classList.remove("active");
    document.body.classList.remove("no-overflow");
}
function addMessage(text, role) {
    const div = document.createElement("div");
    div.classList.add("ai-msg", role);
    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
}

function sendMessage() {
    const text = input.value.trim();
    if (!text) return;
    addMessage(text, "user");
    input.value = "";
    const assistantMessage = addMessage("...", "assistant");
    $.ajax({
        url: `/transparency/card/${cardId}/ask`,
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ question: text }),
        success: function (response) {
            const questionId = response.id;
            pollForAnswer(questionId, assistantMessage);
        },
        error: function (xhr, status, error) {
            let message = "Failed to send question.";
            try {
                const resp = JSON.parse(xhr.responseText);
                message = resp.error || error;
            }
            catch(e) {}
            assistantMessage.classList.add("error");
            assistantMessage.innerText = message;
        }
   });
}

function pollForAnswer(questionId, messageElement) {
    const interval = setInterval(() => {
        $.ajax({
            url: `/transparency/card/${cardId}/ask/${questionId}`,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({}),
            success: function (response) {
                if(response.answer!==undefined && response.answer !== null) messageElement.innerText = response.answer;
                if(response.isfinal===true) clearInterval(interval);
            },
            error: function () {
                clearInterval(interval);
                messageElement.innerText = "Error retrieving answer.";
            }
        });

    }, 1200);
}

askBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", function (e) {
    if(e.key !== "Enter") return;
    e.preventDefault();
    sendMessage();
});
