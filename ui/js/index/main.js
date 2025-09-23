$(function () {
    autocomplete_populate();

    // Check if modal should be skipped
    if (localStorage.getItem('modalDismissed') !== 'true') {
        $('.modal__trigger[data-modal="#modal_help"]').click();
    }

    // Don't show again button
    $('#dontShowAgain').on('click', function() {
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
            url: "http://127.0.0.1:5000/card",
            method: "POST",
            contentType: "application/json",
            headers: {
                "Authorization": "Bearer " + token
            },
            dataType: "json",
            data: JSON.stringify(json),
            success: function (response) {
                window.location.href = 'model_card.html?id=' + response
            },
            error: function (xhr, status, error) {
                alert("ERROR NEW CARD");
            }
        });
    })
});

function autocomplete_populate() {

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
                    const suggestions = response.results.map(item => ({
                        value: item.name, // what will show in dropdown
                        data: {
                            id: item.id,
                            desc: item.desc
                        }
                    }));
                    done({ suggestions: suggestions });
                },
                error: function () {
                    done({ suggestions: [] });
                }
            });
        },
        minChars: 0,          // minimum characters before search
        formatResult: function (suggestion, currentValue) {
            // Highlight search term in the name
            const pattern = new RegExp('(' + $.Autocomplete.utils.escapeRegExChars(currentValue) + ')', 'gi');
            const highlightedName = suggestion.value.replace(pattern, '<strong>$1</strong>');

            // Show description if available
            const desc = suggestion.data.desc ? `<div class="autocomplete-desc">${suggestion.data.desc}</div>` : 'No Description';
            return `<div class="autocomplete-suggestion-item">
                    <div class="autocomplete-name">${highlightedName}<p style="margin: 5px 0 10px 0"> ${desc}</p></div>                   
                </div>`;
        },
        onSelect: function (suggestion) {
            window.location.href = 'model_card.html?id=' + suggestion.data.id;
        }
    });
}
