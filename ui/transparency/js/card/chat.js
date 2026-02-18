
const trigger = document.getElementById("ai-chat-trigger");
const overlay = document.getElementById("ai-chat-overlay");
const closeBtn = document.getElementById("ai-chat-close");

trigger.addEventListener("click", () => {
    overlay.classList.add("active");
    document.body.classList.add("no-overflow");
});

closeBtn.addEventListener("click", () => {
    overlay.classList.remove("active");
    document.body.classList.remove("no-overflow");
});

overlay.addEventListener("click", (e) => {
    if (e.target === overlay) {
        overlay.classList.remove("active");
        document.body.classList.remove("no-overflow");
    }
});