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
                        if ((field.value.trim() !== "") && (field.value.trim() !== "<br>")){
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
            });
        },
        error: function () {
            alert("ERROR GETTING CARD")
        }
    })


    $.when(getToken()).done(function (loginResponse) {
        token = loginResponse.token;

        $.ajax({
            url: "http://127.0.0.1:5000/assistants",
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function (response) {
                const container = document.getElementById("cards-container");
                response.forEach((item, index) => {

                    const htmlString = item.desc;
                    const tempDiv = document.createElement("div");
                    tempDiv.innerHTML = htmlString;

                    const title = tempDiv.querySelector("h1")?.outerHTML || "";
                    tempDiv.querySelector("h1")?.remove();
                    const description = tempDiv.innerText.trim();


                    const card = document.createElement("button");
                    card.id = item.name;
                    card.className = "card-button";
                    if (index === 0) {
                        card.classList.add("selected");
                    }
                    card.innerHTML = `<div class="desc">` + title + `</div><div class="tooltip">` + description + `</div>`;//<h3>${item.name}</h3>
                    container.appendChild(card);
                });

                $('#cards-container').append('<br><p style="margin:12px 0 0px 0px; font-size: 15px; font-weight: 700; color: #1f1f1f;display: inline-block">Actions: </p><p style="display: inline-block;margin:0 5px"><span id="refine">Refine</span> | <span id="autocomplete">Autocomplete: </span> <input type="text" class="text-input" placeholder="Enter URL..." id="card-url" /></p>')

            },
            error: function (e) {
                alert("ERROR GETTING ASSISTANTS")
            }
        })
    }).fail(function () {
        alert("ERROR LOGIN");
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

                ["model", "considerations", "training_set", "eval_set", "analysis"].forEach((sectionName,index) => {
                    let section = cardJson.data.filter(section => section.name !== "related").find(s => s.name === sectionName);
                    let hasValue = false;

                    if (section && section.value) {
                        for (let field of section.value) {
                            if ((field.value.trim() !== "") && (field.value.trim() !== "<br>")){
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
                alert("ERROR EDIT"); //TODO
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
                alert("Error deleting card");
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
        $(".card-button").removeClass("selected");
        $(this).addClass("selected");
    });

    $(document).on("click", "#refine", function () {
        let assistant = $(".card-button.selected").attr("id");

        $.ajax({
            url: "http://127.0.0.1:5000/assistant/" + assistant + '/refine/' + id,
            method: "POST",
            contentType: "application/json",
            dataType: "json",
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function (response) {
                alert(response)
            },
            error: function (xhr, status, error) {
                alert(error); //TODO
            }
        });
    });
    $(document).on("click", "#autocomplete", function () {
        let assistant = $(".card-button.selected").attr("id");

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
                alert(response)
            },
            error: function (xhr, status, error) {
                alert(error); //TODO
            }
        });
    });

});