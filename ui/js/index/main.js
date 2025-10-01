$(function () {
    autocomplete_populate();
    $("#topic").trigger("keyup");
    // Check if modal should be skipped
    if (localStorage.getItem('modalDismissed') !== 'true') {
        $('.modal__trigger[data-modal="#modal_help"]').click();
    }

    // Don't show again button (moved that to the modal close)
//    $('#dontShowAgain').on('click', function () {
//        localStorage.setItem('modalDismissed', 'true');
//        $('.demo-close').click();
//    });
    $('demo-close').on('click', function () {
        localStorage.setItem('modalDismissed', 'true');
        $('.demo-close').click();
    });

    $(".input-effect input").on("input", function () {
        if ($(this).val() !== "") {
            $(this).addClass("has-content");
            $('#new_card_but').attr("disabled", false)
        } else {
            $(this).removeClass("has-content");
            $('#new_card_but').attr("disabled", true)
        }
    })

    $('#new_card_but').click(function () {

        if ($(this).attr("disabled")) return;

        const json = {"title": $('#model_name_input').val()}
        $.ajax({
            url: "http://127.0.0.1:5000/card", method: "POST", contentType: "application/json", headers: {
                "Authorization": "Bearer " + token
            }, dataType: "json", data: JSON.stringify(json), success: function (response) {
                window.location.href = 'model_card.html?id=' + response
            }, error: function (xhr, status, error) {
                alert("ERROR NEW CARD");
            }
        });
    })
});

function autocomplete_populate() {/*

    $('#topic').autocomplete({
        lookup: function (query, done) {
            // AJAX call to your server
            $.ajax({
                url: "http://127.0.0.1:5000/cards",
                method: "POST",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify({
                    query: query
                }),
                success: function (response) {
                    // Transform your response into plugin format
                    let suggestions = response.results.map(item => ({
                        value: item.name, // what will show in dropdown
                        data: {
                            id: item.id,
                            desc: item.desc
                        }
                    }));
                    /!*if (suggestions.length === 0) {
                        suggestions = [{
                            value: "No matching results",
                            data: { id: null, desc: "" },
                            noResult: true
                        }];
                    }*!/
                    done({ suggestions: suggestions });
                },
                error: function () {
                    done({ suggestions: [] });
                }
            });
        },
        showNoSuggestionNotice:true,
        minChars: 0,          // minimum characters before search
        deferRequestBy: 150,
        formatResult: function (suggestion, currentValue) {

            /!*!/!*if (suggestion.noResult) {
                return `<div class="autocomplete-noresult" style="pointer-events: none">${suggestion.value}</div>`;
            }*!/

            // Highlight search term in the name
            const pattern = new RegExp('(' + $.Autocomplete.utils.escapeRegExChars(currentValue) + ')', 'gi');
            const highlightedName = suggestion.value.replace(pattern, '<strong>$1</strong>');

            // Show description if available
            const desc = suggestion.data.desc ? `<div class="autocomplete-desc">${suggestion.data.desc}</div>` : 'No Description';
            return `<div class="autocomplete-suggestion-item">
                    <div class="autocomplete-name">${highlightedName}<p style="margin: 5px 0 10px 0"> ${desc}</p></div>                   
                </div>`;*!/
        },
        onSelect: function (suggestion) {
           /!* if (suggestion.noResult) {
                // prevent selecting the "No matching results" item
                return false;
            }*!/
            window.location.href = 'model_card.html?id=' + suggestion.data.id;
        }
    });*/

    let typingTimer;
    const delay = 400; // ms delay after typing stops

    $("#topic").on("keyup", function () {
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
                    const results = response.results || [];
                    const $tbody = $("#resultsTable tbody");
                    $tbody.empty();

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
                                "<strong>$1</strong>"
                            );

                            $tbody.append(`
                                <tr style="background: #1F1F1F;" class="search_results_button">
                                    <td><a style="width: 160px;text-decoration:none" href="model_card.html?id=${item.id}"><span style="width: 300px; display: block; color: #EEEEEE;">${highlightedName}</span> <span style="font-size: 13px; color: #79CFDC;">${item.desc+" - by "+item.creator || "No Description"}</span></td>

                                </tr>
                            `);
                        });
                        $("#resultsTable").show();
                    } else {
                        $tbody.append(`
                            <tr><td colspan="3" style="text-align:center; color:#888;">No matching results</td></tr>
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
