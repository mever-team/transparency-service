$(function () {
    $('#loading').show();
    autocomplete_populate();
    $("#topic").trigger("keyup");
    if (localStorage.getItem('modalDismissed') !== 'true')
        $('.modal__trigger[data-modal="#modal_help"]').click();
    $('demo-close').on('click', () => {
        localStorage.setItem('modalDismissed', 'true');
        $('.demo-close').click();
    });
    $('#new_card').click(() => {
        $.ajax({
            url: "http://127.0.0.1:5000/card",
            method: "POST",
            contentType: "application/json",
            headers: { "Authorization": "Bearer " + token },
            data: JSON.stringify({ title: "" }),
            success: r => window.location.href = 'model_card.html?id=' + r,
            error: () => alert("ERROR NEW CARD")
        });
    });
});

function autocomplete_populate() {
    let lastUpdate = 0, pending = null, first = true, delay = 150;
    const $topic = $("#topic"), $tbody = $("#resultsTable tbody");

    function request() {
        const q = $topic.val().trim();
        if (first) $('#loading').show();
        $.ajax({
            url: "http://127.0.0.1:5000/cards",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ query: q }),
            success: r => {
                $('#loading').hide();
                const results = r.results || [];
                $('#search_results_wrapper').text(q ? "Showing results for" : "Showing most popular");
                $('#search_results').text(results.length + " in total " + (r.total || 0));
                $tbody.empty();
                if (results.length)
                    results.forEach(it => {
                        const name = it.name.replace(new RegExp("(" + q + ")", "ig"), "<strong style='color:#79CFDC'>$1</strong>");
                        $tbody.append(`
                            <tr class="search_results_button">
                                <td><a style="width:160px;text-decoration:none" href="model_card.html?id=${it.id}">
                                    <span style="width:300px;display:block;color:#EEE">${name}</span>
                                    <span style="font-size:13px;color:#79CFDC">${it.desc + " --by " + it.creator || "No Description"}</span>
                                </a></td>
                            </tr>`);
                    });
                else
                    $tbody.append(`<tr><td colspan="3" style="text-align:center;color:#EEEEEE;font-weight:bold;font-size:22px;">No matching results</td></tr>`);
                $("#resultsTable").show();
                first = false;
            },
            error: () => { $('#loading').hide(); first = false; console.error("Error fetching results"); }
        });
    }

    $topic.on("keyup", () => {
        const now = Date.now();
        if (now - lastUpdate < delay && !first) {
            clearTimeout(pending);
            pending = setTimeout(request, delay);
            return;
        }
        lastUpdate = now;
        request();
    });
}
