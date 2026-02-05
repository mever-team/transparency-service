var cardJson;
var comparedJson;
var menuOffsetTop=0;

function error_message(message) {
    console.log(message);
    document.getElementById('popup-error-screen').style.display = 'flex';
    if(message) document.getElementById('error-message').innerHTML = message;
}

function error_handler(xhr, status, error) {
    try {
        const resp = JSON.parse(xhr.responseText);
        error_message(resp.error || error);
    }
    catch(e) { error_message(""); }
}

// Close confirmation modal
document.getElementById('cancel-delete-btn').onclick = function () {document.getElementById('delete-confirm-screen').style.display = 'none';};
document.getElementById('cancel-autocomplete-btn').onclick = function () {document.getElementById('modal-autocomplete-screen').style.display = 'none';};
document.getElementById('cancel-refine-btn').onclick = function () {document.getElementById('modal-refine-screen').style.display = 'none';};

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
    let menuOffsetTop = $menu.offset().top; // this will be updated, depending on history taking up space
    const pageUrl = encodeURIComponent(window.location.href);
    const pageTitle = encodeURIComponent(document.title);
    $('#pdf_desc').hide();
    $("#share-x").attr("href", `https://twitter.com/intent/tweet?url=${pageUrl}&text=${pageTitle}`);
    $("#share-facebook").attr("href", `https://www.facebook.com/sharer/sharer.php?u=${pageUrl}`);
    $("#share-linkedin").attr("href", `https://www.linkedin.com/shareArticle?mini=true&url=${pageUrl}&title=${pageTitle}`);
    $("#share-whatsapp").attr("href", `https://wa.me/?text=${pageUrl}`);
    $("#share-telegram").attr("href", `https://t.me/share/url?url=${pageUrl}&text=${pageTitle}`);

    $('#pdf_text').click(function () {
        $('#pdf_text,#card-url,#card-url-p').slideUp();
        $('.upload-container,#url_text').slideDown();
        $('#url_desc').slideUp();
        $('#pdf_desc').slideDown();
    })
    $('#url_text').click(function () {
        $('#pdf_text,#card-url,#card-url-p').slideDown();
        $('.upload-container,#url_text').slideUp();
        $('#url_desc').slideDown();
        $('#pdf_desc').slideUp();
    })

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > menuOffsetTop - 20) $menu.addClass('fixed');
        else $menu.removeClass('fixed');
    });

    let interval = setInterval(function () {checkLocked(interval);}, 100); // do first run immediately
    function runRefinement(assistant, id) {
        $.ajax({
            url: "/transparency/assistant/" + assistant + '/refine/' + id,
            method: "POST",
            contentType: "application/json",
            dataType: "json",
            headers: {"Authorization": "Bearer " + token},
            success: function (response) {},
            error: error_handler
        });
    }
    function checkLocked(interval) {
        $.ajax({
            url: "/transparency/card/" + id + "/locked",
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
                        $("#model-pending").html(jsonData.description?"":"DRAFT (needs version to be searchable)");
                        $("#model-quality").html(`
                             <svg class="quality-circle" viewBox="0 0 36 36">
                              <circle cx="18" cy="18" r="18" fill="none" stroke="#434343" stroke-width="3"/>
                              <circle cx="18" cy="18" r="18" fill="none" stroke="${jsonData.quality>0.7?'#6CC06B':jsonData.quality>0.4?'#FBC483':'#F87F76'}" stroke-width="3"
                                stroke-dasharray="100" stroke-dashoffset="${100 - Math.round(jsonData.quality * 100)}"/>
                              <text x="18" y="14" class="quality-text"> ${Math.round(jsonData.quality * 100)}%</text>
                              <text x="18" y="24" class="quality-text">info</text>
                            </svg>
                        `);

                        const historyContainer = document.getElementById("history-dropdown");
                        historyContainer.innerHTML = ""; // clear previous content
                        if (jsonData.history) {
                            renderHistoryGraph(
                                jsonData.history,
                                Number(id),
                                historyContainer
                            );
                            menuOffsetTop = $menu.offset().top;
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
                                    $fieldValue.append($("<option>").val("").text("—").prop({
                                        selected: true,disabled: true,hidden: true}));
                                    const options = field.type.replace("list:", "").split(",");
                                    let $currentGroup = null;
                                    options.forEach(opt => {
                                        if (opt.startsWith("#")) {
                                            $currentGroup = $("<optgroup>").attr("label", opt.replace("#", ""));
                                            $fieldValue.append($currentGroup);
                                        } else {
                                            const $option = $("<option>").val(opt).text(opt);
                                            if (field.value === opt) $option.prop("selected", true);
                                            // Append to optgroup if it exists, otherwise directly to select
                                            if ($currentGroup) $currentGroup.append($option);
                                            else $fieldValue.append($option);
                                        }
                                    });
                                } else if (field.type === 'date') {
                                    $fieldValue = $("<input>", {type: "date", readonly: token? false: true}).addClass("field-value").val(field.value || "");
                                    $fieldValue.on("change", function () {field.value = $(this).val();});
                                    if(token) $fieldValue.attr("contenteditable", "true");
                                    
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
                        if (!($('.light.arrow').length > 0)&& token) {
                            // TODO: we have the option of just opening the import, which may be more practical
                            document.getElementById('modal-autocomplete-screen').style.display = 'flex';
                        }
                    }

                    if(compareto) {
                        $.ajax({
                            url: "/transparency/card/" + compareto,
                            method: "GET",
                            contentType: "application/json",
                            dataType: "json",
                            success: function (jsonData) {
                                comparedJson = jsonData;
                                render();
                            },
                            error: function (xhr, status, error) {}
                        });
                    }
                    else
                        comparedJson = {}; // we use the existence of comparedJson as a mark for render()
                    $.ajax({
                        url: "/transparency/card/" + id,
                        method: "GET",
                        contentType: "application/json",
                        dataType: "json",
                        success: function (jsonData) {
                            cardJson = jsonData;
                            render();
                        },
                        error: error_handler
                    });

                }
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    if (interval) clearInterval(interval);
                    $('#model-title').remove();
                    $('#loading').hide();
                    $('#loading').hide();
                    $('#share-options').hide();
                    $('#edit-options').hide();
                    $('#deleteCard').hide();
                    $('.example_button').css('pointer-events', 'none');
                    if(resp.error || error) error_handler(xhr, status, error);
                } catch (e) { error_message(""); }
            }
        });
    }

    if(token)
        $.ajax({
            url: "/transparency/assistants",
            method: "GET",
            headers: {"Authorization": "Bearer " + token},
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
            error: error_handler
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
                if(field.type.startsWith("list:")) field.value = $(this).find(":selected").val();
                else field.value = $(this).html();
            }
        }
    });

    if(token) $("#edit-options").show();

    $("#saveJson").click(function () {
        $("#saveJson").fadeOut();
        $.ajax({
            url: "/transparency/card/" + id,
            method: "PUT",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(cardJson.data.filter(section => section.name !== "history")),
            headers: {"Authorization": "Bearer " + token},
            success: function (response) {
                $('.menu').find('div').find('.light').removeClass('arrow');
                $('.menu').find('div').find('.light').addClass('square');

                ["overview", "use", "training", "evaluation", "performance", "safety"].forEach((sectionName, index) => {
                    let section = cardJson.data.filter(section => section.name !== "history").find(s => s.name === sectionName);
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
                $("#model-pending").html(response.description?"":"DRAFT (needs version to be searchable)");
                $("#model-quality").html(`
                     <svg class="quality-circle" viewBox="0 0 36 36">
                      <circle cx="18" cy="18" r="18" fill="none" stroke="#434343" stroke-width="3"/>
                      <circle cx="18" cy="18" r="18" fill="none" stroke="${response.quality>0.7?'#6CC06B':response.quality>0.4?'#FBC483':'#F87F76'}" stroke-width="3"
                        stroke-dasharray="100" stroke-dashoffset="${100 - Math.round(response.quality * 100)}"/>
                      <text x="18" y="14" class="quality-text"> ${Math.round(response.quality * 100)}%</text>
                      <text x="18" y="24" class="quality-text">info</text>
                    </svg>
                `);
                const historyContainer = document.getElementById("history-dropdown");
                historyContainer.innerHTML = ""; // clear previous content
                if (response.history) {
                    renderHistoryGraph(
                        response.history,
                        Number(id),
                        historyContainer
                    );
                }
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
            error: error_handler
        });
    });

    const downloadBtn = document.getElementById("downloadCard");
    const downloadMenu = document.getElementById("downloadDropdown");

    downloadBtn.addEventListener("click", function() {
        const isOpen = downloadMenu.style.display === "block";
        downloadMenu.style.display = isOpen ? "none" : "block";
        if(isOpen) return;
        const closeMenu = (event) => {
            if(downloadBtn.contains(event.target)) return;
            if(downloadMenu.contains(event.target)) return;
            downloadMenu.style.display = "none";
            document.removeEventListener("click", closeMenu);
        }
        document.addEventListener("click", closeMenu);
    });

    downloadMenu.addEventListener("click", e => {
        downloadMenu.style.display = "none";
        const item = e.target.closest(".download-dropdown-item");
        const format = item.getAttribute("data-format");
        const url = "/transparency/card/" + id + "/download/" + format
        $.ajax({
            url: url,
            method: "GET",
            success: function (response) {window.location = url},
            error: error_handler
        });
    });

    const assistBtn = document.getElementById("assistCard");
    const assistMenu = document.getElementById("assistDropdown");
    assistBtn.addEventListener("click", function() {
        const isOpen = assistMenu.style.display === "block";
        assistMenu.style.display = isOpen ? "none" : "block";
        if(isOpen) return;
        const closeMenu = (event) => {
            if(assistBtn.contains(event.target)) return;
            if(assistMenu.contains(event.target)) return;
            assistMenu.style.display = "none";
            document.removeEventListener("click", closeMenu);
        };
        document.addEventListener("click", closeMenu);
    });
    assistMenu.addEventListener("click", function(e) {
        const item = e.target.closest(".download-dropdown-item, .modal_autocomplete, .modal_refine");
        if(!item) return;
        assistMenu.style.display = "none";
        if(item.classList.contains("modal_autocomplete")) document.getElementById('modal-autocomplete-screen').style.display = 'flex';
        else if(item.classList.contains("modal_refine")) document.getElementById('modal-refine-screen').style.display = 'flex';
    });

    $("#cardClone").click(function () {
        if(!token) {
            error_message("You must be logged in to clone a card. Either your session expired or the service temporarily became unavailable, and you need to log in again.");
            return;
        }
        $("#cardClone").prop("disabled", true).text("Cloning...");
        $.ajax({
            url: "/transparency/card/" + id + "/clone",
            method: "POST",
            contentType: "application/json",
            headers: { "Authorization": "Bearer " + token },
            success: function (newId) {window.location.href = "model_card.html?id=" + newId;},
            error: function (xhr, status, error) {
                $("#cardClone").prop("disabled", false).text("Clone");
                error_handler(xhr, status, error);
            }
        });
    });

    $("#modal_autocomplete").click(function () {document.getElementById('modal-autocomplete-screen').style.display = 'flex';});
    $("#modal_refine").click(function () { document.getElementById('modal-refine-screen').style.display = 'flex';});
    $("#deleteCard").click(function () {document.getElementById('delete-confirm-screen').style.display = 'flex';});
    $(".delete-confirm-screen").click(function (e) { if ($(e.target).is(this)) $(this).hide();});
    document.getElementById('confirm-delete-btn').onclick = function () {
        document.getElementById('delete-confirm-screen').style.display = 'none';
        $.ajax({
            url: "/transparency/card/" + id, // replace id
            method: "DELETE",
            headers: {"Authorization": "Bearer " + token},
            success: function (response) {
                const screen = document.getElementById('delete-success-screen');
                screen.style.display = 'flex';
                document.getElementById('close-success-btn').onclick = function () { screen.style.display = 'none'; }
            },
            error: error_handler
        });
    };

    $(document).on("click", ".card-button", function () {
        if ($(this).parents('#modal-refine-screen').length) {
            const assistant = $(this).attr("id");
            document.getElementById('modal-refine-screen').style.display = 'none';
            $.ajax({
                url: "/transparency/card/" + id,
                method: "PUT",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(cardJson.data.filter(s => s.name !== "history")),
                headers: { "Authorization": "Bearer " + token },
                success: function () {
                    $.ajax({
                        url: "/transparency/card/" + id + "/clone",
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
                url: "/transparency/card/" + id,
                method: "PUT",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(cardJson.data.filter(section => section.name !== "history")),
                headers: {"Authorization": "Bearer " + token},
                success: function (response) {
                    $('.menu').find('div').find('.light').removeClass('arrow');
                    $('.menu').find('div').find('.light').addClass('square');

                    ["overview", "use", "training", "evaluation", "performance", "safety"].forEach((sectionName, index) => {
                        let section = cardJson.data.filter(section => section.name !== "history").find(s => s.name === sectionName);
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
                            url: "/transparency/assistant/" + assistant + '/complete/' + id,
                            method: "POST",
                            contentType: "application/json",
                            dataType: "json",
                            headers: { "Authorization": "Bearer " + token},
                            data: JSON.stringify($('#card-url').val()),
                            success: function (response) {
                                document.getElementById('modal-autocomplete-screen').style.display = 'none';
                                interval = setInterval(function () {checkLocked(interval);}, 1);
                            },
                            error: function (xhr, status, error) {
                                document.getElementById('modal-autocomplete-screen').style.display = 'none';
                                error_handler(xhr, status, error);
                            }
                        });
                    } else {
                        let formData = new FormData();
                        formData.append("file", uploaded_file); // "file" is the field name your backend expects
                        $.ajax({
                            url: "/transparency/assistant/" + assistant + '/complete/' + id,
                            method: "POST",
                            headers: {
                                "Authorization": "Bearer " + token
                            },
                            data: formData,
                            processData: false, // don't let jQuery process the data
                            contentType: false, // don't set content-type header, let browser set it (multipart/form-data)
                            success: function (response) {
                                document.getElementById('modal-autocomplete-screen').style.display = 'none';
                                interval = setInterval(function () {checkLocked(interval);}, 1);
                                //alert(response)
                            },
                            error: function (xhr, status, error) {
                                document.getElementById('modal-autocomplete-screen').style.display = 'none';
                                error_handler(xhr, status, error);
                            }
                        });
                    }
                },
                error: function (xhr, status, error) {
                    document.getElementById('modal-autocomplete-screen').style.display = 'none';
                    error_handler(xhr, status, error);
                }
            });
        }
    });
});
