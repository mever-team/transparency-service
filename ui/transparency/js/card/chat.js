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

                                console.log(response)
                                if (energy_consumed && emissions) {
                                    let phone_charge_equivalent = formatHours(Number(energy_consumed) / 0.02) // the argument is in hours assuming a charger consumes 20W
                                    energy_consumed = formatKWh(energy_consumed);
                                    emissions = formatKg(emissions);

                                    const text = `Job finished with energy consumed <strong>${energy_consumed}</strong> and CO2 emissions ${emissions}. This is equal to <strong>${phone_charge_equivalent}</strong> of fast phone charging.`;
                                    console.log(text);
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

    function formatHours(hours) {
        const totalSeconds = Math.round(hours * 3600);

        const h = Math.floor(totalSeconds / 3600);
        const m = Math.floor((totalSeconds % 3600) / 60);
        const s = totalSeconds % 60;

        const parts = [];

        if (h > 0) parts.push(`${h} hour${h !== 1 ? "s" : ""}`);
        if (m > 0) parts.push(`${m} minute${m !== 1 ? "s" : ""}`);
        if (s > 0) parts.push(`${s} second${s !== 1 ? "s" : ""}`);

        return parts.length > 0 ? parts.join(" and ") : "0 seconds";
    }

    function formatKWh(kWh) {
        const wh = kWh * 1000;
        const units = [
            { name: 'TWh', factor: 1e12 },
            { name: 'GWh', factor: 1e9 },
            { name: 'MWh', factor: 1e6 },
            { name: 'kWh', factor: 1e3 },
            { name: 'Wh',  factor: 1 },
            { name: 'mWh', factor: 1e-3 },
            { name: 'μWh', factor: 1e-6 },
            { name: 'nWh', factor: 1e-9 },
            { name: 'pWh', factor: 1e-12 }
        ];

        let bestUnit = units[units.length - 1]; // fallback to smallest
        let bestValue = wh / bestUnit.factor;

        for (const unit of units) {
            const value = wh / unit.factor;
            if (value >= 1 && value < 1000) {
            bestUnit = unit;
            bestValue = value;
            break;
            }
        }

        const formattedNumber = (Math.abs(bestValue - Math.round(bestValue)) < 1e-10)
            ? Math.round(bestValue).toString()
            : bestValue.toFixed(2).replace(/\.?0+$/, '');

        return `${formattedNumber} ${bestUnit.name}`;
    }

    function formatKg(kg) {
        const grams = kg * 1000;
        const units = [
            { name: 'Mt',   factor: 1e12 },
            { name: 'kt',   factor: 1e9 },
            { name: 't',    factor: 1e6 },
            { name: 'kg',   factor: 1e3 },
            { name: 'g',    factor: 1 },
            { name: 'mg',   factor: 1e-3 },
            { name: 'μg',   factor: 1e-6 },
            { name: 'ng',   factor: 1e-9 }
        ];

        let bestUnit = units[units.length - 1];
        let bestValue = grams / bestUnit.factor;

        for (const unit of units) {
            const value = grams / unit.factor;
            if (value >= 1 && value < 1000) {
            bestUnit = unit;
            bestValue = value;
            break;
            }
        }

        const formatted = (Math.abs(bestValue - Math.round(bestValue)) < 1e-10)
            ? Math.round(bestValue).toString()
            : bestValue.toFixed(2).replace(/\.?0+$/, '');
        return `${formatted} ${bestUnit.name}`;
    }
});