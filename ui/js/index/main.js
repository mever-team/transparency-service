$(function () {
    $('#loading').show();
    autocomplete_populate();
    $("#topic").trigger("keyup");
    if (localStorage.getItem('modalDismissed') !== 'true') {
        $('.modal__trigger[data-modal="#modal_help"]').click();
    }
    $('demo-close').on('click', function () {
        localStorage.setItem('modalDismissed', 'true');
        $('.demo-close').click();
    });
    $('#new_card').click(function () {
        $.ajax({
            url: "http://127.0.0.1:5000/card",
            method: "POST",
            contentType: "application/json",
            headers: {
                "Authorization": "Bearer " + token
            },
            dataType: "json",
            data: JSON.stringify({ "title": "" }),
            success: function (response) {
                window.location.href = 'model_card.html?id=' + response;
            },
            error: function () {
                alert("ERROR NEW CARD");
            }
        });
    });
});


function autocomplete_populate() {
    let lastUpdateTime = 0;
    const delay = 150; // milliseconds
    let firstLoad = true;

    $("#topic").on("keyup", function () {
        const $tbody = $("#resultsTable tbody");
        const query = $(this).val().trim();
        const now = Date.now();

        // Only update if enough time has passed since the last request
        if (now - lastUpdateTime < delay && !firstLoad) {
            return; // Skip this keyup event
        }

        lastUpdateTime = now; // Record when this update started

        // Show loading only for the first autocomplete
        if (firstLoad) $('#loading').show();

        $.ajax({
            url: "http://127.0.0.1:5000/cards",
            method: "POST",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({ query: query }),
            success: function (response) {
                $('#loading').hide();
                const results = response.results || [];

                if ($("#topic").val().trim() !== "") {
                    $('#search_results_wrapper').text("Search results");
                } else {
                    $('#search_results_wrapper').text("Most popular");
                }

                $('#search_results').text(results.length+" of "+(response.total||0));
                $tbody.empty();
                if (results.length > 0) {
                    results.forEach(item => {
                        const highlightedName = item.name.replace(
                            new RegExp("(" + query + ")", "ig"),
                            "<strong style='color:#79CFDC'>$1</strong>"
                        );

                        $tbody.append(`
                            <tr style="background: #1F1F1F;" class="search_results_button">
                                <td>
                                    <a style="width: 160px; text-decoration:none" href="model_card.html?id=${item.id}">
                                        <span style="width: 300px; display: block; color: #EEEEEE;">${highlightedName}</span>
                                        <span style="font-size: 13px; color: #79CFDC;">${item.desc + " - by " + item.creator || "No Description"}</span>
                                    </a>
                                </td>
                            </tr>
                        `);
                    });
                    $("#resultsTable").show();
                } else {
                    $tbody.append(`
                        <tr><td colspan="3" style="text-align: center; color: #1f1f1f; font-weight: bold; font-size: 22px;">No matching results</td></tr>
                    `);
                    $("#resultsTable").show();
                }

                firstLoad = false; // only first time shows loading
            },
            error: function () {
                $('#loading').hide();
                console.error("Error fetching results");
                firstLoad = false;
            }
        });
    });
}
