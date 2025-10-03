var cardJson;

// Show delete confirmation
function showDeleteConfirm() {
    document.getElementById('delete-confirm-screen').style.display = 'flex';
}

// Close confirmation modal
document.getElementById('cancel-delete-btn').onclick = function () {
    document.getElementById('delete-confirm-screen').style.display = 'none';
};

$(document).on("click", ".naccs .menu div", function () {
    var numberIndex = $(this).index();

    if (!$(this).is("active")) {
        $(".naccs .menu div").removeClass("active");
        $(".naccs ul li").removeClass("active");

        $(this).addClass("active");
        $(".naccs ul").find("li:eq(" + numberIndex + ")").addClass("active");

        /* var listItemHeight = $(".naccs ul")
             .find("li:eq(" + numberIndex + ")")
             .innerHeight();
         $(".naccs ul").height(listItemHeight + "px");*/
    }
});

$(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    const $menu = $('.menu');
    const menuOffsetTop = $menu.offset().top;

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > menuOffsetTop - 20) {
            $menu.addClass('fixed');
        } else {
            $menu.removeClass('fixed');
        }
    });

    let interval = setInterval(function () {
        checkLocked(interval, true);
    }, 500);

    function checkLocked(interval) {
        $.ajax({
            url: "http://127.0.0.1:5000/card/" + id + "/locked",
            method: "GET",
            contentType: "application/json",
            dataType: "json",
            success: function (jsonData) {
                if (jsonData !== "") {
                    document.getElementById('card-locked').style.display = 'flex';
                    $('#lock-msg-text').html(jsonData);
                    $('body').addClass('no-overflow');
                } else {
                    $('body').removeClass('no-overflow');
                    document.getElementById('card-locked').style.display = 'none';
                    if (interval) {
                        clearInterval(interval);
                    }

                    $.ajax({
                        url: "http://127.0.0.1:5000/card/" + id,
                        method: "GET",
                        contentType: "application/json",
                        dataType: "json",
                        success: function (jsonData) {
                            cardJson = jsonData;
                            //$("#model-title").text("Model Card: " + jsonData.title);
                            $("#model-title").text(jsonData.title);
                            const $ul = $(".nacc");
                            $ul.empty();
                            $('#loading').hide();
                            jsonData.data.forEach((section, index) => {
                                let sectionTitle = section.name.replace(/_/g, " ").toUpperCase();

                                let $li = $("<li>").toggleClass("active", index === 0);
                                let $section = $("<section>");
                                $section.append($("<h2>").text(sectionTitle));

                                if (section.value.length > 0) {

                                    section.value.forEach(field => {
                                        let $field = $("<div>").addClass("field");
                                        $field.append($("<span>").addClass("field-name").text(field.name.replace(/_/g, " ") + ":"));

                                        // Editable field value
                                        let $fieldValue = $("<span>")
                                            .addClass("field-value editable")
                                            .attr("contenteditable", "true")
                                            .html(field.value || "");
                                        if ((field.value.trim() !== "") && (field.value.trim() !== "<br>")) {
                                            $('.menu').find('div').eq(index).find('.light').removeClass('square');
                                            $('.menu').find('div').eq(index).find('.light').addClass('arrow');
                                        }
                                        $field.append($fieldValue);
                                        $section.append($field);

                                    });
                                } else {
                                    $section.append($("<p>").text("No data provided."));
                                }

                                $li.append($("<div>").append($section));
                                $ul.append($li);
                                $('.menu').find('div').removeClass('active');
                                $('.menu div:first-child').addClass('active');

                            });
                        },
                        error: function (xhr, status, error) {
                            try {
                                const resp = JSON.parse(xhr.responseText);
                                //alert(resp.error || error); An AI assistant is working on the card
                            } catch (e) {
                                alert("Unknown card submission error");
                            }
                        }
                    })

                }
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);

                    if (interval) {
                        clearInterval(interval);
                    }
                    $('#model-title').remove();
                    $('#loading').hide();
                    $('.nacc').append('<l1 class="empty_card">⚠️'+(resp.error || error)+'</l1>')
                    $('.example_button').css('pointer-events','none');
                } catch (e) {
                    alert("Unknown card lock error");
                }
            }
        });
    }

    $.when(getToken()).done(function (loginResponse) {
        token = loginResponse.token;

        $.ajax({
            url: "http://127.0.0.1:5000/assistants",
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function (response) {

                $(".assistants_wrapper").each(function () {
                    const $container = $(this);

                    $.each(response, function (index, item) {
                        const $tempDiv = $("<div>").html(item.desc);

                        const title = $tempDiv.find("h1").prop("outerHTML") || "";
                        $tempDiv.find("h1").remove();
                        const description = $.trim($tempDiv.text());

                        if (index === 0) {
                            $('#selected_autofilled_assistant,#selected_refined_assistant').text($("<div>").html(title).text())
                        }

                        const $card = $("<button>", {
                            id: item.name,
                            class: "card-button" + (index === 0 ? " selected" : ""),
                            html: `<div class="desc">${title}</div><div class="tooltip">${description}</div>`
                        });

                        $container.append($card);
                    });
                });

                /* $('#cards-container').append('<br><p style="margin:12px 0 0px 0px; font-size: 15px; font-weight: 700; color: #1f1f1f;display: inline-block">Actions: </p><p style="display: inline-block;margin:0 5px"><span id="refine">Refine</span> | <span id="autocomplete">Autocomplete: </span> <input type="text" class="text-input" placeholder="Enter URL..." id="card-url" /></p>')
 */
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    alert(resp.error || error);
                } catch (e) {
                    alert("Unknown card retrieval error");
                }
            }
        })
    }).fail(function (xhr, status, error) {
        try {
            const resp = JSON.parse(xhr.responseText);
            alert(resp.error || error);
        } catch (e) {
            alert("Unknown login error");
        }
    });

    $(".nacc").on("input", ".editable", function () {
        const fieldName = $(this).siblings(".field-name").text().replace(":", "").toLowerCase().replace(/ /g, "_");
        const sectionName = $(this).closest("section").find("h2").text().toLowerCase().replace(/ /g, "_");

        // Find section + field in jsonData and update value
        let section = cardJson.data.find(s => s.name === sectionName);
        if (section) {
            let field = section.value.find(f => f.name === fieldName);
            if (field) {
                field.value = $(this).html();
            }
        }
    });

    $("#saveJson").click(function () {
        $('#saveJson').attr("disabled", true)
        $.ajax({
            url: "http://127.0.0.1:5000/card/" + id,
            method: "PUT",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(cardJson.data.filter(section => section.name !== "related")),
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function (response) {
                $('.menu').find('div').find('.light').removeClass('arrow');
                $('.menu').find('div').find('.light').addClass('square');

                ["model", "considerations", "training_set", "eval_set", "analysis"].forEach((sectionName, index) => {
                    let section = cardJson.data.filter(section => section.name !== "related").find(s => s.name === sectionName);
                    let hasValue = false;

                    if (section && section.value) {
                        for (let field of section.value) {
                            if ((field.value.trim() !== "") && (field.value.trim() !== "<br>")) {
                                hasValue = true;
                                $('.menu').find('div').eq(index).find('.light').removeClass('square');
                                $('.menu').find('div').eq(index).find('.light').addClass('arrow');
                                break; // stop at first non-empty
                            }
                        }
                    }
                });

                $("#saveJson").find('.btn-text').hide();
                $("#saveJson").find('.btn-confirmation').fadeIn();

                // Restore after 2s
                setTimeout(function () {
                    $("#saveJson").find('.btn-confirmation').fadeOut(function () {
                        $("#saveJson").find('.btn-text').fadeIn();
                        $('#saveJson').attr("disabled", false)
                    });
                }, 1500);
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    alert(resp.error || error);
                } catch (e) {
                    alert(error || xhr.responseText);
                }
            }
        });
    });

    $("#deleteCard").click(function () {
        showDeleteConfirm();
    });
    document.getElementById('confirm-delete-btn').onclick = function () {
        document.getElementById('delete-confirm-screen').style.display = 'none';

        // Call AJAX DELETE
        $.ajax({
            url: "http://127.0.0.1:5000/card/" + id, // replace id
            method: "DELETE",
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function (response) {
                showDeleteSuccess();
                // optionally remove the card from DOM
            },
            error: function (xhr, status, error) {
                //alert("Error deleting card");
                try {
                    const resp = JSON.parse(xhr.responseText);
                    alert(resp.error || error);
                } catch (e) {
                    alert("Unknown error at deleting card");
                }
            }
        });
    };

// Show success overlay
    function showDeleteSuccess() {
        const screen = document.getElementById('delete-success-screen');
        screen.style.display = 'flex';

        document.getElementById('close-success-btn').onclick = function () {
            screen.style.display = 'none';
        }

        // Optional auto-dismiss
        /* setTimeout(() => { screen.style.display = 'none'; }, 3000);*/
    }

    $(document).on("click", ".card-button", function () {


        // If it's already selected AND it's the only selected, do nothing
        if ($(this).hasClass("selected") && $(".card-button.selected").length === 1) {
            return; // prevent unselecting the last one
        }

        // Otherwise, unselect all and select this one
        $(this).parent().find(".card-button").removeClass("selected");
        $(this).addClass("selected");
        if (($(this).parents('#modal_autocomplete').length)) {
            $('#selected_autofilled_assistant').text($(this).find('h1').text());
        } else {
            $('#selected_refined_assistant').text($(this).find('h1').text());
        }

    });

    $(document).on("click", "#refine", function () {
        let assistant = $(this).prev('.assistants_wrapper').find(".card-button.selected").attr("id");
        $('.modal__close ').click();
        $.ajax({
            url: "http://127.0.0.1:5000/card/" + id,
            method: "PUT",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(cardJson.data.filter(section => section.name !== "related")),
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function (response) {
                $('.menu').find('div').find('.light').removeClass('arrow');
                $('.menu').find('div').find('.light').addClass('square');

                ["model", "considerations", "training_set", "eval_set", "analysis"].forEach((sectionName, index) => {
                    let section = cardJson.data.filter(section => section.name !== "related").find(s => s.name === sectionName);
                    let hasValue = false;

                    if (section && section.value) {
                        for (let field of section.value) {
                            if ((field.value.trim() !== "") && (field.value.trim() !== "<br>")) {
                                hasValue = true;
                                $('.menu').find('div').eq(index).find('.light').removeClass('square');
                                $('.menu').find('div').eq(index).find('.light').addClass('arrow');
                                break; // stop at first non-empty
                            }
                        }
                    }
                });

                $.ajax({
                    url: "http://127.0.0.1:5000/assistant/" + assistant + '/refine/' + id,
                    method: "POST",
                    contentType: "application/json",
                    dataType: "json",
                    headers: {
                        "Authorization": "Bearer " + token
                    },
                    success: function (response) {

                        interval = setInterval(function () {
                            checkLocked(interval);
                        }, 500);
                    },
                    error: function (xhr, status, error) {
                        try {
                            const resp = JSON.parse(xhr.responseText);
                            alert(resp.error || error);
                        } catch (e) {
                            alert("Unknown refinement error");
                        }
                    }
                });
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    alert(resp.error || error);
                } catch (e) {
                    alert(error || xhr.responseText);
                }
            }
        });
    });

    $(document).on("click", "#autocomplete", function () {
        let assistant = $(this).siblings('.assistants_wrapper').find(".card-button.selected").attr("id");

        $('#saveJson').attr("disabled", true)
        $.ajax({
            url: "http://127.0.0.1:5000/card/" + id,
            method: "PUT",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(cardJson.data.filter(section => section.name !== "related")),
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function (response) {
                $('.menu').find('div').find('.light').removeClass('arrow');
                $('.menu').find('div').find('.light').addClass('square');

                ["model", "considerations", "training_set", "eval_set", "analysis"].forEach((sectionName, index) => {
                    let section = cardJson.data.filter(section => section.name !== "related").find(s => s.name === sectionName);
                    let hasValue = false;

                    if (section && section.value) {
                        for (let field of section.value) {
                            if ((field.value.trim() !== "") && (field.value.trim() !== "<br>")) {
                                hasValue = true;
                                $('.menu').find('div').eq(index).find('.light').removeClass('square');
                                $('.menu').find('div').eq(index).find('.light').addClass('arrow');
                                break; // stop at first non-empty
                            }
                        }
                    }
                });

                if ($('#card-url').is(":visible")) {
                    $.ajax({
                        url: "http://127.0.0.1:5000/assistant/" + assistant + '/complete/' + id,
                        method: "POST",
                        contentType: "application/json",
                        dataType: "json",
                        headers: {
                            "Authorization": "Bearer " + token
                        },
                        data: JSON.stringify($('#card-url').val()),
                        success: function (response) {
                            $('.modal__close ').click();
                            interval = setInterval(function () {
                                checkLocked(interval);
                            }, 500);
                        },
                        error: function (xhr, status, error) {
                            try {
                                const resp = JSON.parse(xhr.responseText);
                                alert(resp.error || error);
                            } catch (e) {
                                alert("Unknown autocomplete error");
                            }
                        }
                    });
                } else {
                    let formData = new FormData();
                    formData.append("file", uploaded_file); // "file" is the field name your backend expects
                    $.ajax({
                        url: "http://127.0.0.1:5000/assistant/" + assistant + '/complete/' + id,
                        method: "POST",
                        headers: {
                            "Authorization": "Bearer " + token
                        },
                        data: formData,
                        processData: false, // don't let jQuery process the data
                        contentType: false, // don't set content-type header, let browser set it (multipart/form-data)
                        success: function (response) {
                            alert(response)
                        },
                        error: function (xhr, status, error) {
                            try {
                                const resp = JSON.parse(xhr.responseText);
                                alert(resp.error || error);
                            } catch (e) {
                                alert("Unknown card creation error");
                            }
                        }
                    });
                }
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    alert(resp.error || error);
                } catch (e) {
                    alert(error || xhr.responseText);
                }
            }
        });
    });

    $('#pdf_text').click(function () {
        $('#pdf_text,#card-url,#card-url-p').slideUp();
        $('.upload-container,#url_text').slideDown();
    })

    $('#url_text').click(function () {
        $('#pdf_text,#card-url,#card-url-p').slideDown();
        $('.upload-container,#url_text').slideUp();
    })

});