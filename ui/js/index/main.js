$(function () {
    autocomplete_populate();
    $("#topic").trigger("keyup");
    // Check if modal should be skipped
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
            data: JSON.stringify({"title":""}),
            success: function(response) {
                window.location.href = 'model_card.html?id=' + response
            },
            error: function(xhr, status, error) {
                alert("ERROR NEW CARD");
            }
        });
    })
});

function autocomplete_populate() {

    let typingTimer;
    const delay = 400; // ms delay after typing stops

    $("#topic").on("keyup", function () {
        const $tbody = $("#resultsTable tbody");
        $tbody.empty();
        $('#loading').show();
        clearTimeout(typingTimer);
        const query = $(this).val().trim();

        /*if (query.length === 0) {
            $("#resultsTable").hide().find("tbody").empty();
            return;
        }*/

        typingTimer = setTimeout(function () {

            $.ajax({
                url: "http://127.0.0.1:5000/cards",
                method: "POST",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify({
                    query: query
                }),
                success: function (response) {
                    $('#loading').hide();
                    const results = response.results || [];


                    if ($("#topic").val().trim() !== "") {
                        $('#search_results_wrapper').text("Search results")
                    } else {
                        $('#search_results_wrapper').text("Most popular")
                    }
                    $('#search_results').text(results.length)
                    if (results.length > 0) {

                        results.forEach(item => {

                            let highlightedName = item.name.replace(
                                new RegExp("(" + query + ")", "ig"),
                                "<strong style='color:#79CFDC'>$1</strong>"
                            );

                            $tbody.append(`
                                <tr style="background: #1F1F1F;" class="search_results_button">
                                    <td><a style="width: 160px;text-decoration:none" href="model_card.html?id=${item.id}"><span style="width: 300px; display: block; color: #EEEEEE;">${highlightedName}</span> <span style="font-size: 13px; color: #79CFDC;">${item.desc + " - by " + item.creator || "No Description"}</span></td>

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
                },
                error: function () {
                    console.error("Error fetching results");
                }
            });
        }, delay);
    });


}
