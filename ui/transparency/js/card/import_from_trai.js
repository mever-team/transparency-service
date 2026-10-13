$(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    const $input = $('#modal-autocomplete-screen #trai-url')
    const $importError = $('#import-error');
    $(document).on('click', '.card-button#agent[data-type="trai"]', request);


    function request(){
        const url = $input.val();
        const srcId = extractTrAIId(url);
        if (Number.isInteger(id) && id > 0){
            $importError.text(srcId);
            $importError.show();
            return
        }
        $.ajax({
            url: "/transparency/importFromTraiCard/" + srcId + '/' + id,
            method: "POST",
            contentType: "application/json",
            headers: { "Authorization": "Bearer " + token },
            success: function () {
                window.location.reload();
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    $importError.text(resp.error || error);
                    $importError.show();
                }
                catch(e) { 
                    $importError.text('Something went wrong.');
                    $importError.show();
                }}
        });

    }

    function extractTrAIId(url) {
        try {
            const parsed = new URL(
                url.startsWith("http://") || url.startsWith("https://")
                    ? url
                    : "https://" + url
            );

            if (parsed.hostname !== "trai.mever.gr") {
                return "The URL must belong to trai.mever.gr.";
            }

            if (parsed.pathname !== "/transparency/model_card.html") {
                return "The URL must point to /transparency/model_card.html.";
            }

            if (!parsed.searchParams.has("id")) {
                return "The URL must contain a model card ID.";
            }

            const id = parsed.searchParams.get("id");

            if (!/^\d+$/.test(id) || Number(id) <= 0) {
                return "The model card ID must be a positive integer.";
            }

            return Number(id);
        } catch {
            return "Invalid URL.";
        }
    }


    function error_message(message) {
        console.log(message);
        $('#popup-error-screen').css('display' , 'flex');
        if(message) $('#error-message').html(message);
    }

    function error_handler(xhr, status, error) {
        try {
            const resp = JSON.parse(xhr.responseText);
            error_message(resp.error || error);
        }
        catch(e) { error_message(""); }
    }
})