var topics_csv = [];


$(function () {
    autocomplete_populate();
    examples_populate();


    $(window).scroll(function (e) {
        var $el = $('.main_search_wrapper');
        if (($(window).scrollTop() > $el.offset().top)) {
            $('.dummy_input').show();
            $el.addClass('fixed_input');
        }

        if (($(window).scrollTop() < $('.search_main_p').offset().top)) {
            $el.removeClass('fixed_input');
            $('.dummy_input').hide();
        }
    });

    $(".input-effect input").on("input", function () {
        if ($(this).val() != "") {
            $(this).addClass("has-content");
            $('#new_card_but').attr("disabled", false)
        } else {
            $(this).removeClass("has-content");
            $('#new_card_but').attr("disabled", true)
        }
    })

    $('#pdf_text').click(function () {
        $('#pdf_text,.input-effect').slideUp();
        $('.upload-container').slideDown();
        $('#new_card_but').hide();
    })
    $(".examples_section").on("click", ".example_button", function () {
        window.location.href = 'model_card.html?id=' + $(this).attr('data-id');
    });
    $('#new_card_but').click(function () {

        if ($(this).attr("disabled")) return;

        if (!($('.upload-container').is(":visible"))) {

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
        }
    })
});

function autocomplete_populate() {

    $.ajax({
        url: "http://127.0.0.1:5000/cards",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            query: "",
            page_size: 10000,
            page: 1
        }),
        success: function (response) {
            let count = response.results.length;

            if (count < 10) {
                $('.search_sub_p span').text(count);
            } else {
                $('.search_sub_p span').text((Math.floor(count / 10) * 10) + "+");
            }

            response.results.forEach(function (item) {
                topics_csv.push({
                    "value": item.name,
                    "id": item.id
                });
            });
        },
        error: function (xhr, status, error) {
            alert("ERROR AUTOCOMPLETE");//TODO
        }
    });


    $('#topic').devbridgeAutocomplete({
        lookup: topics_csv,
        minChars: 0,
        beforeRender: function () {
            $('.autocomplete-suggestion').each(function () {
                if ($(this).next().hasClass('autocomplete-group')) {
                    $(this).css('margin-bottom', '15px')
                }
            });
        },
        onSelect: function (suggestion) {
            var $topic = $('#topic');
            $topic.val("");
            $topic.blur();
            window.location.href = 'model_card.html?id=' + suggestion.id;

        },
        showNoSuggestionNotice: true,
        noSuggestionNotice: 'Sorry, no matching models cards'
    });
}

function examples_populate() {

    $.ajax({
        url: "http://127.0.0.1:5000/cards",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            query: "",
            page_size: 10,
            page: 1
        }),
        success: function (response) {
            $("#examples_wrapper").empty();

            // Loop through results and add to the <ul>
            response.results.forEach(function (item) {
                const match = item.desc.match(/(\d+)%?/);
                const percentage = match ? parseInt(match[1], 10) : 0;
                /*const listItem = `<li><strong></strong>: ${item.desc} (ID: ${item.id})<a href="model_card.html?id=${item.id}">View</a></li>`;*/
                const listItem = `<div class="example_wrapper"> <div class="example_cell"> <div class="example_title"><h3>${item.name}</h3></div> </div> <div class="example_cell"> <div class="example_count"> <p>${item.desc}</p> <div class="progress"> <div class="progress-bar" style="width: ${percentage}%"></div>  </div> </div> </div> <div class="example_cell"> <div class="example_button" data-id="${item.id}"> View </div> </div> </div>`;
                $("#examples_wrapper").append(listItem);
            });
        },
        error: function (xhr, status, error) {
            alert("ERROR EXAMPLES"); //TODO
        }
    });
}

function uploadFile(file) {
    let formData = new FormData();
    formData.append("file", file); // "file" is the field name your backend expects

    $.ajax({
        url: "http://127.0.0.1:5000/card",
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        },
        data: formData,
        processData: false, // don't let jQuery process the data
        contentType: false, // don't set content-type header, let browser set it (multipart/form-data)
        success: function (response) {
            window.location.href = 'model_card.html?id=' + response;
        },
        error: function (xhr, status, error) {
            alert("ERROR NEW CARD: " + xhr.responseText);
        }
    });
}