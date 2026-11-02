import {formatHours, formatKWh, formatKg} from './card.js'

$(function() {
    const trigger = document.getElementById("ai-chat-trigger");
    const overlay = document.getElementById("ai-chat-overlay");
    const closeBtn = document.getElementById("ai-chat-close");
    const input = document.getElementById("ai-chat-input");
    const askBtn = document.getElementById("ai-chat-ask");
    const messages = document.getElementById("ai-chat-messages");
    const urlParams = new URLSearchParams(window.location.search);
    const cardId = urlParams.get('id');

    $(trigger).on("click", () => {
        overlay.classList.add("active");
        document.body.classList.add("no-overflow");
    });
    $(closeBtn).on("click", closeChat);
    $(overlay).on("click", (e) => {if (e.target === overlay) closeChat();});

    function closeChat() {
        overlay.classList.remove("active");
        document.body.classList.remove("no-overflow");
    }
    function addMessage(text, role) {
        const div = document.createElement("div");
        div.classList.add("ai-msg", role);
        div.innerHTML = text;
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
                assistantMessage.innerHTML = message;
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
                    if(response.answer!==undefined && response.answer !== null) messageElement.innerHTML = response.answer;
                    if(response.isfinal===true) {
                        $.ajax({
                            url: "/transparency/emissions/" + cardId + '/chat/flash',
                            method: "GET",
                            contentType: "application/json",
                            dataType: "json",
                            success: function (response) {
                                let energy_consumed = response['energy_consumed'];
                                let emissions = response['emissions'];
                                if (energy_consumed && emissions) {
                                    let phone_charge_equivalent = formatHours(Number(energy_consumed) / 0.02) // the argument is in hours assuming a charger consumes 20W
                                    energy_consumed = formatKWh(energy_consumed);
                                    emissions = formatKg(emissions);

                                    const energy_text = `Answer consumed ${energy_consumed} and CO2 emissions ${emissions}. This is equal to ${phone_charge_equivalent} of fast phone charging.`;
                                    const energy_tooltip = $('<span>')
                                                            .css({
                                                                background: 'none',
                                                                color: 'var(--text-primary)',
                                                                transform: 'translate(8px, 8px)',
                                                                'z-index': 10000,
                                                                position: 'absolute',
                                                                'font-size': '1rem',
                                                            })
                                                            .addClass('info-tooltip')
                                                            .attr('data-tooltip', energy_text)
                                                            .html('ⓘ');
                                    $(messageElement).before(energy_tooltip)
                                    messageElement.innerHTML = '<br>' + messageElement.innerHTML
                                }
                            },
                            error: function (xhr, status, error) {
                                try {
                                    const resp = JSON.parse(xhr.responseText);
                                    console.log(resp.error || error);
                                }
                                catch(e) { console.log(""); }
                            }
                        });
                        clearInterval(interval);
                    }
                },
                error: function () {
                    clearInterval(interval);
                    messageElement.innerHTML = "Error retrieving answer.";
                }
            });

        }, 1200);
    }
    
    $(askBtn).on("click", sendMessage);
    $(input).on("keydown", function (e) {
        if(e.key !== "Enter") return;
        e.preventDefault();
        sendMessage();
    });
});