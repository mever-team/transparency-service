var cardJson;
var comparedJson;
var empty_card_flag=true;

// Close confirmation modal
document.getElementById('cancel-delete-btn').onclick = function () {document.getElementById('delete-confirm-screen').style.display = 'none';};
document.getElementById('manual-fill-card').onclick = function () {document.getElementById('empty_card_screen').style.display = 'none';};
document.getElementById('cancel-autocomplete-btn').onclick = function () {document.getElementById('modal-autocomplete-screen').style.display = 'none';};
document.getElementById('cancel-refine-btn').onclick = function () {document.getElementById('modal-refine-screen').style.display = 'none';};
document.getElementById('assistant-fill-card').onclick = function () {
    document.getElementById('empty_card_screen').style.display = 'none';
    document.getElementById('modal-autocomplete-screen').style.display = 'flex';
};

$(document).on("click", ".naccs .menu div", function () {
    let numberIndex = $(this).index();
    if (!$(this).is("active")) {
        $(".naccs .menu div").removeClass("active");
        $(".naccs ul li").removeClass("active");
        $(".naccs ul").children("li").eq(numberIndex).addClass("active");
        $(this).addClass("active");
    }
});

$(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    const compareto = urlParams.get('compareto');
    const $menu = $('.menu');
    const menuOffsetTop = $menu.offset().top;

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > menuOffsetTop - 20) {
            $menu.addClass('fixed');
        } else {
            $menu.removeClass('fixed');
        }
    });

    let interval = setInterval(function () {checkLocked(interval);}, 100); // do first run immediately

    function runRefinement(assistant, id) {
        $.ajax({
            url: "/assistant/" + assistant + '/refine/' + id,
            method: "POST",
            contentType: "application/json",
            dataType: "json",
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function (response) {
                //interval = setInterval(function () {checkLocked(interval);}, 500);
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    //alert(resp.error || error);
                } catch (e) {
                    //alert("Unknown refinement error");
                }
            }
        });
    }
    function checkLocked(interval) {
        $.ajax({
            url: "/card/" + id + "/locked",
            method: "GET",
            contentType: "application/json",
            dataType: "json",
            success: function (jsonData) {
                if (jsonData !== "") {
                    document.getElementById('card-locked').style.display = 'flex';
                    $('#lock-msg-text').html(jsonData);
                    $('body').addClass('no-overflow');
                    $('#loading').hide();
                } else {
                    $('body').removeClass('no-overflow');
                    document.getElementById('card-locked').style.display = 'none';
                    if (interval) clearInterval(interval);

                    function render() {
                        if(!cardJson || !comparedJson) return;
                        let jsonData = cardJson;
                        $("#model-title").text(jsonData.title);
                        $("#model-description").html(jsonData.description);

                        const historyContainer = document.getElementById("history-dropdown");
                        historyContainer.innerHTML = ""; // clear previous content

                        // create card buttons
                        if (jsonData.related && Object.keys(jsonData.related).length > 0) {
                            const wrapper = document.createElement("div");
                            wrapper.className = "related-wrapper";

                            const sortedKeys = Object.keys(jsonData.related).sort();
                            const smallestKey = sortedKeys[0];
                            const smallestText = jsonData.related[smallestKey] || smallestKey;

                            const button = document.createElement("div");
                            button.className = "related_button";
                            button.textContent = `${smallestText} ▾`;

                            const dropdown = document.createElement("div");
                            dropdown.className = "download-dropdown-menu related-dropdown";
                            dropdown.style.display = "none";

                            Object.entries(jsonData.related).forEach(([key, rel]) => {
                                const item = document.createElement("div");
                                item.className = "download-dropdown-item";
                                item.textContent = rel || key;
                                item.addEventListener("click", () => {
                                    window.location.href = `model_card.html?id=${key}`;
                                });
                                dropdown.appendChild(item);
                            });

                            button.addEventListener("click", () => {
                                const open = dropdown.style.display === "block";
                                dropdown.style.display = open ? "none" : "block";
                                if (!open) {
                                    const closeMenu = (e) => {
                                        if (!button.contains(e.target) && !dropdown.contains(e.target)) {
                                            dropdown.style.display = "none";
                                            document.removeEventListener("click", closeMenu);
                                        }
                                    };
                                    document.addEventListener("click", closeMenu);
                                }
                            });
                            wrapper.append(button, dropdown);
                            historyContainer.appendChild(wrapper);
                        }

                        // fill in fields
                        const $ul = $(".nacc");
                        $ul.empty();
                        $('#loading').hide();
                        jsonData.data.forEach((section, index) => {
                            let baseSection = comparedJson&&comparedJson.data?comparedJson.data[index]:undefined;
                            let sectionTitle = section.name.replace(/_/g, " ").toUpperCase();
                            let $li = $("<li>").toggleClass("active", index === 0);
                            let $section = $("<section>");
                            $section.append($("<h2>").text(sectionTitle));
                            if (!section.value.length) $section.append($("<p>").text("No data provided."));
                            section.value.forEach((field, fieldIndex) => {
                                let $field = $("<div>").addClass("field");

                                // field-name
                                let $fieldName = $("<span>")
                                    .addClass("field-name")
                                    .text(" "+field.name.replace(/_/g, " "));

                                // info-tooltip
                                let $fieldInfo = $("<span>")
                                    .addClass("info-tooltip")
                                    .attr("data-tooltip", field.description)
                                    .text("?");
                                $fieldInfo = $("<span>").addClass("field-info").append($fieldInfo).append($fieldName);
                                let $fieldValue;
                                if (field.type.startsWith("list:") && token) {
                                    $fieldValue = $("<select>").addClass("field-value dropdown");
                                    const options = field.type.replace("list:", "").split(",");
                                    options.forEach(opt => {
                                        const $option = $("<option>").val(opt).text(opt);
                                        if (field.value === opt) $option.prop("selected", true);
                                        $fieldValue.append($option);
                                    });
                                } else {
                                    $fieldValue = $("<span>") .addClass("field-value").html(field.value || "");
                                    if(token) $fieldValue.attr("contenteditable", "true");
                                }
                                if(token) $fieldValue.addClass("editable");

                                // Editable field value
                                if ((field.value.trim() !== "") && (field.value.trim() !== "<br>") && (field.value.trim() !== "unknown")) {
                                    $('.menu').find('div').eq(index).find('.light').removeClass('square');
                                    $('.menu').find('div').eq(index).find('.light').addClass('arrow');
                                }

                                $field.append($fieldInfo).append($fieldValue);
                                $section.append($field);

                                // compared value
                                if(baseSection) {
                                    console.log(baseSection.value[fieldIndex]);
                                    let $baseFieldValue = $("<span>")
                                            .addClass("field-value")
                                            .html(baseSection.value[fieldIndex].value || "");

                                    let $fieldBase = $("<span>")
                                        .addClass("field-name")
                                        .text("Original");

                                    $field.append($fieldBase);
                                    $field.append($baseFieldValue);
                                }
                            });

                            $li.append($("<div>").append($section));
                            $ul.append($li);
                            $('.menu').find('div').removeClass('active');
                            $('.menu div:first-child').addClass('active');

                        });
                        if (!($('.light.arrow').length > 0)&& empty_card_flag && token) {
                            document.getElementById('empty_card_screen').style.display = 'flex';
                            empty_card_flag=false;
                        }
                        else
                            empty_card_flag=false;
                    }

                    if(compareto) {
                        $.ajax({
                            url: "/card/" + compareto,
                            method: "GET",
                            contentType: "application/json",
                            dataType: "json",
                            success: function (jsonData) {
                                comparedJson = jsonData;
                                render();
                            },
                            error: function (xhr, status, error) {
                                try {
                                    const resp = JSON.parse(xhr.responseText);
                                }
                                catch (e) {
                                }
                            }
                        });
                    }
                    else
                        comparedJson = {}; // we use the existence of comparedJson as a mark for render()
                    $.ajax({
                        url: "/card/" + id,
                        method: "GET",
                        contentType: "application/json",
                        dataType: "json",
                        success: function (jsonData) {
                            cardJson = jsonData;
                            render();
                        },
                        error: function (xhr, status, error) {
                            try {
                                const resp = JSON.parse(xhr.responseText);
                                //alert(resp.error || error); An AI assistant is working on the card
                            } catch (e) {
                                //alert("Unknown card submission error");
                            }
                        }
                    });

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
                    $('.nacc').append('<l1 class="empty_card">⚠️' + (resp.error || error) + '</l1>')
                    $('.example_button').css('pointer-events', 'none');
                } catch (e) {
                    //alert("Unknown card lock error");
                }
            }
        });
    }

    if(token)
        $.ajax({
            url: "/assistants",
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
                        const $card = $("<button>", {
                            id: item.name,
                            class: "card-button",
                            html: `<div class="desc">${title}</div><div class="tooltip">${description}</div>`
                        });

                        $container.append($card);
                    });
                });
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    //alert(resp.error || error);
                } catch (e) {
                    //alert("Unknown card retrieval error");
                }
            }
        });

    $(".nacc").on("input", ".editable", function () {
        const fieldName = $(this).siblings(".field-info").contents()[1].outerText.replace(":", "").trim().toLowerCase().replace(/ /g, "_");
        const sectionName = $(this).closest("section").find("h2").contents().filter((_, el) => el.nodeType === 3).text().toLowerCase().replace(/ /g, "_");

        // Find section + field in jsonData and update value
        let section = cardJson.data.find(s => s.name === sectionName);
        if (section) {
            let field = section.value.find(f => f.name === fieldName);
            $("#saveJson").fadeIn();
            if (field) {
                if(field.type.startsWith("list:")){
                    field.value = $(this).find(":selected").val();
                }
                else{
                    field.value = $(this).html();
                }

            }
        }
    });

    if(token)
        $("#edit-options").show();

    $("#saveJson").click(function () {
        $("#saveJson").fadeOut();
        $.ajax({
            url: "/card/" + id,
            method: "PUT",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(cardJson.data.filter(section => section.name !== "related")),  // TODO: we no have related, but we may have history inthe future
            headers: {
                "Authorization": "Bearer " + token
            },
            success: function (response) {
                $('.menu').find('div').find('.light').removeClass('arrow');
                $('.menu').find('div').find('.light').addClass('square');

                ["model", "considerations", "training_set", "eval_set", "performance", "safety"].forEach((sectionName, index) => {
                    let section = cardJson.data.filter(section => section.name !== "related").find(s => s.name === sectionName);
                    let hasValue = false;

                    if (section && section.value) {
                        for (let field of section.value) {
                            if ((field.value.trim() !== "") && (field.value.trim() !== "<br>") && (field.value.trim() !== "unknown")) {
                                hasValue = true;
                                $('.menu').find('div').eq(index).find('.light').removeClass('square');
                                $('.menu').find('div').eq(index).find('.light').addClass('arrow');
                                break; // stop at first non-empty
                            }
                        }
                    }
                });

                $("#model-title").text(response.title);
                $("#model-description").html(response.description);
//
//                // TODO: enable once it does not crash new card creation
//                const history<Container = document.getElementById("history-dropdown");
//                historyContainer.innerHTML = ""; // clear previous content>
//                if (jsonData.related && Object.keys(jsonData.related).length > 0) {
//                    const wrapper = document.createElement("div");
//                    wrapper.className = "related-wrapper";
//
//                    // find smallest key (string order)
//                    const sortedKeys = Object.keys(jsonData.related).sort();
//                    const smallestKey = sortedKeys[0];
//                    const smallestText = jsonData.related[smallestKey] || smallestKey;
//
//                    const button = document.createElement("div");
//                    button.className = "related_button";
//                    button.textContent = `${smallestText} ▾`; // ✅ show first related entry before the arrow
//
//                    const dropdown = document.createElement("div");
//                    dropdown.className = "download-dropdown-menu related-dropdown";
//                    dropdown.style.display = "none";
//
//                    Object.entries(jsonData.related).forEach(([key, rel]) => {
//                        const item = document.createElement("div");
//                        item.className = "download-dropdown-item";
//                        item.textContent = rel || key;
//                        item.addEventListener("click", () => {
//                            window.location.href = `model_card.html?id=${key}`;
//                        });
//                        dropdown.appendChild(item);
//                    });
//
//                    button.addEventListener("click", () => {
//                        const open = dropdown.style.display === "block";
//                        dropdown.style.display = open ? "none" : "block";
//
//                        if (!open) {
//                            const closeMenu = (e) => {
//                                if (!button.contains(e.target) && !dropdown.contains(e.target)) {
//                                    dropdown.style.display = "none";
//                                    document.removeEventListener("click", closeMenu);
//                                }
//                            };
//                            document.addEventListener("click", closeMenu);
//                        }
//                    });
//
//                    wrapper.append(button, dropdown);
//                    historyContainer.appendChild(wrapper);
//                }

                $("#saveJson").find('.btn-text').hide();
                $("#saveJson").find('.btn-confirmation').fadeIn();

                // Restore after 2s
                setTimeout(function () {
                    $("#saveJson").find('.btn-confirmation').fadeOut(function () {
                        $("#saveJson").find('.btn-text').fadeIn();
                        $("#saveJson").fadeOut();
                        //$('#saveJson').attr("disabled", false)
                    });
                }, 1500);
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    //alert(resp.error || error);
                } catch (e) {
                    //alert(error || xhr.responseText);
                }
            }
        });
    });

    const downloadBtn = document.getElementById("downloadCard");
    const downloadMenu = document.getElementById("downloadDropdown");

    downloadBtn.addEventListener("click", function() {
        const isOpen = downloadMenu.style.display === "block";
        downloadMenu.style.display = isOpen ? "none" : "block";

        if (!isOpen) {
            const closeMenu = (event) => {
                if (!downloadBtn.contains(event.target) && !downloadMenu.contains(event.target)) {
                    downloadMenu.style.display = "none";
                    document.removeEventListener("click", closeMenu);
                }
            };
            document.addEventListener("click", closeMenu);
        }
    });

    downloadMenu.addEventListener("click", e => {
        downloadMenu.style.display = "none";

        const item = e.target.closest(".download-dropdown-item");

        const format = item.getAttribute("data-format");
        const url = "/card/" + id + "/download/" + format

        $.ajax({
            url: url,
            method: "GET",
            success: function (response) {
                window.location = url
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    //alert(resp.error || error);
                } catch (e) {
                    //alert("Unknown error downloading card");
                }
            }
        });
    });


    const assistBtn = document.getElementById("assistCard");
    const assistMenu = document.getElementById("assistDropdown");
    assistBtn.addEventListener("click", function() {
        const isOpen = assistMenu.style.display === "block";
        assistMenu.style.display = isOpen ? "none" : "block";
        if (!isOpen) {
            const closeMenu = (event) => {
                if (!assistBtn.contains(event.target) && !assistMenu.contains(event.target)) {
                    assistMenu.style.display = "none";
                    document.removeEventListener("click", closeMenu);
                }
            };
            document.addEventListener("click", closeMenu);
        }
    });
    assistMenu.addEventListener("click", function(e) {
        const item = e.target.closest(".download-dropdown-item, .modal_autocomplete, .modal_refine");
        if (!item) return;
        assistMenu.style.display = "none";
        if (item.classList.contains("modal_autocomplete")) {
            document.getElementById('modal-autocomplete-screen').style.display = 'flex';
        }
        else if (item.classList.contains("modal_refine")) {
            document.getElementById('modal-refine-screen').style.display = 'flex';
        }
    });

    $("#cardClone").click(function () {
        if (!token) {
            //alert("You must be logged in to clone a card.");
            return;
        }
        $("#cardClone").prop("disabled", true).text("Cloning...");
        $.ajax({
            url: "/card/" + id + "/clone",
            method: "POST",
            contentType: "application/json",
            headers: { "Authorization": "Bearer " + token },
            success: function (newId) {
                window.location.href = "model_card.html?id=" + newId;
            },
            error: function (xhr, status, error) {
                $("#cardClone").prop("disabled", false).text("Clone");
                try {
                    const resp = JSON.parse(xhr.responseText);
                    //alert(resp.error || "Error cloning card");
                } catch (e) {
                    //alert("Unknown error cloning card");
                }
            }
        });
    });

    $("#modal_autocomplete").click(function () {
        document.getElementById('modal-autocomplete-screen').style.display = 'flex';
    });

    $("#modal_refine").click(function () {
        document.getElementById('modal-refine-screen').style.display = 'flex';
    });

    $("#deleteCard").click(function () {
        document.getElementById('delete-confirm-screen').style.display = 'flex';
    });
    $(".delete-confirm-screen").click(function (e) {
        if ($(e.target).is(this)) {
            $(this).hide();
        }
    });
    document.getElementById('confirm-delete-btn').onclick = function () {
        document.getElementById('delete-confirm-screen').style.display = 'none';

        // Call AJAX DELETE
        $.ajax({
            url: "/card/" + id, // replace id
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
                    //alert(resp.error || error);
                } catch (e) {
                    //alert("Unknown error at deleting card");
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
        if ($(this).parents('#modal-refine-screen').length) {
            const assistant = $(this).attr("id");
            document.getElementById('modal-refine-screen').style.display = 'none';
            $.ajax({
                url: "/card/" + id,
                method: "PUT",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(cardJson.data.filter(s => s.name !== "related")),
                headers: { "Authorization": "Bearer " + token },
                success: function () {
                    $.ajax({
                        url: "/card/" + id + "/clone",
                        method: "POST",
                        headers: { "Authorization": "Bearer " + token },
                        success: function (newId) {
                            runRefinement(assistant, newId);
                            window.open("model_card.html?id=" + newId, "_blank");
                        }
                    });
                }
            });
            return;
        }
        else {
            let assistant = $(this).attr("id");
            $("#saveJson").find('.btn-confirmation').fadeOut();

            $.ajax({
                url: "/card/" + id,
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

                    ["model", "considerations", "training_set", "eval_set", "performance", "safety"].forEach((sectionName, index) => {
                        let section = cardJson.data.filter(section => section.name !== "related").find(s => s.name === sectionName);
                        let hasValue = false;

                        if (section && section.value) {
                            for (let field of section.value) {
                                if ((field.value.trim() !== "") && (field.value.trim() !== "<br>") && (field.value.trim() !== "unknown")) {
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
                            url: "/assistant/" + assistant + '/complete/' + id,
                            method: "POST",
                            contentType: "application/json",
                            dataType: "json",
                            headers: {
                                "Authorization": "Bearer " + token
                            },
                            data: JSON.stringify($('#card-url').val()),
                            success: function (response) {
                                document.getElementById('modal-autocomplete-screen').style.display = 'none';
                                interval = setInterval(function () {
                                    checkLocked(interval);
                                }, 1);
                            },
                            error: function (xhr, status, error) {
                                document.getElementById('modal-autocomplete-screen').style.display = 'none';
                                try {
                                    const resp = JSON.parse(xhr.responseText);
                                    //alert(resp.error || error);
                                } catch (e) {
                                    //alert("Unknown autocomplete error");
                                }
                            }
                        });
                    } else {
                        let formData = new FormData();
                        formData.append("file", uploaded_file); // "file" is the field name your backend expects
                        $.ajax({
                            url: "/assistant/" + assistant + '/complete/' + id,
                            method: "POST",
                            headers: {
                                "Authorization": "Bearer " + token
                            },
                            data: formData,
                            processData: false, // don't let jQuery process the data
                            contentType: false, // don't set content-type header, let browser set it (multipart/form-data)
                            success: function (response) {
                                document.getElementById('modal-autocomplete-screen').style.display = 'none';
                                //alert(response)
                            },
                            error: function (xhr, status, error) {
                                document.getElementById('modal-autocomplete-screen').style.display = 'none';
                                try {
                                    const resp = JSON.parse(xhr.responseText);
                                    //alert(resp.error || error);
                                } catch (e) {
                                    //alert("Unknown card creation error");
                                }
                            }
                        });
                    }
                },
                error: function (xhr, status, error) {
                    document.getElementById('modal-autocomplete-screen').style.display = 'none';
                    try {
                        const resp = JSON.parse(xhr.responseText);
                        //alert(resp.error || error);
                    } catch (e) {
                        //alert(error || xhr.responseText);
                    }
                }
            });


        }
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



const pageUrl = encodeURIComponent(window.location.href);
const pageTitle = encodeURIComponent(document.title);

document.getElementById("share-x").href = `https://twitter.com/intent/tweet?url=${pageUrl}&text=${pageTitle}`;
document.getElementById("share-facebook").href = `https://www.facebook.com/sharer/sharer.php?u=${pageUrl}`;
document.getElementById("share-linkedin").href = `https://www.linkedin.com/shareArticle?mini=true&url=${pageUrl}&title=${pageTitle}`;
document.getElementById("share-whatsapp").href = `https://wa.me/?text=${pageUrl}`;
document.getElementById("share-telegram").href = `https://t.me/share/url?url=${pageUrl}&text=${pageTitle}`;