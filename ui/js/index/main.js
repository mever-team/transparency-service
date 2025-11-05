$(function () {
    $('#loading').show();
    const lastSearch = localStorage.getItem("last_search_term") || "";
    $("#topic").val(lastSearch);
    autocomplete_populate();
    $("#topic").trigger("keyup");
    if (localStorage.getItem('modalDismissed') !== 'true')
        $('.modal__trigger[data-modal="#modal_help"]').click();

    $('body').on('click', '.demo-close', function () {
        localStorage.setItem('modalDismissed', 'true');
    });
    $('#new_card').click(() => {
        $.ajax({
            url: "/card",
            method: "POST",
            contentType: "application/json",
            headers: { "Authorization": "Bearer " + token },
            data: JSON.stringify({ title: "" }),
            success: r => window.location.href = 'model_card.html?id=' + r,
            error: () => alert("ERROR NEW CARD")
        });
    });

    $(document).on('click', '.dropdown-btn', function(e) {
        e.stopPropagation();
        $(this).parent().toggleClass('show');
    });

    $(document).on('click', function() {
        $('.dropdown-filter').removeClass('show');
    });

    $(document).on('click', '.dropdown-content a', function (e) {
        e.preventDefault();
        const text = $(this).text().trim().toLowerCase();
        const tag = `${text}`;
        const $input = $('#topic');
        const currentVal = $input.val();

        // Only add tag if not already present
        if (!currentVal.includes(tag)) {
            $input.val(currentVal + (currentVal ? ' ' : '') + tag + ' ');
        }

        $input.focus();
    })

});

function autocomplete_populate() {
    let lastUpdate = 0, pending = null, first = true, delay = 150;
    const $topic = $("#topic"), $tbody = $("#resultsTable tbody");

    function request() {
        const q = $topic.val().trim();
        if (first) $('#loading').show();
        $.ajax({
            url: "/cards",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ query: q }),
            success: r => {
                $('#loading').hide();
                const results = r.results || [];
                $('#search_results_wrapper').text(q ? "Found" : "Most popular");
                $('#search_results').text(results.length + " of " + (r.total || 0));
                $tbody.empty();
                if (results.length)
                    results.forEach(it => {
                        const name = it.name.replace(new RegExp("(" + q + ")", "ig"), "<strong style='color:#79CFDC'>$1</strong>");
                        $tbody.append(`
                            <tr class="search_results_button">
                                <td><a style="display:block;width:100%;height:100%;text-decoration:none" href="model_card.html?id=${it.id}">
                                    <span style="width:300px;display:block;color:#EEE">${name}</span>
                                    <span style="font-size:13px;color:#79CFDC">${it.desc + " by " + it.creator || "No Description"}</span>
                                </a></td>
                            </tr>`);
                    });
                else
                    $tbody.append(`<tr><td colspan="3" style="text-align:center;color:#EEEEEE;font-weight:bold;font-size:22px;">No matching results</td></tr>`);
                $("#resultsTable").show();
                localStorage.setItem("last_search_term", $("#topic").val());
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


document.getElementById('login-confirm-btn').onclick = function () {
    let json = {
        "password": document.getElementById('username').value,
        "username": document.getElementById('password').value
    }
    $.ajax({
        url: "/login",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(json),
        success: function (response) {
            token = response.token;
            updateUsername();
            document.getElementById('login-confirm-screen').style.display = 'none';
        },
        error: function (xhr, status, error) {
            token = "";
            updateUsername();
            try {
                $('#login-error').text("Failed to login: "+xhr.responseJSON.error);
            } catch (e) {
                $('#login-error').text(xhr||"Server is offline");
            }
        }
    });
};

document.getElementById('login-btn').onclick = function () {
    document.getElementById('login-error').text = "";
    document.getElementById('login-confirm-screen').style.display = 'flex';
};
document.getElementById('logout-btn').onclick = function () {
    token = "";
    updateUsername();
};
document.getElementById('cancel-login-btn').onclick = function () {
    document.getElementById('login-error').text = "";
    document.getElementById('login-confirm-screen').style.display = 'none';
};

document.addEventListener("DOMContentLoaded", () => {
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const loginBtn = document.getElementById("login-confirm-btn");

    function submitOnEnter(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            loginBtn.click();
        }
    }

    username.addEventListener("keydown", submitOnEnter);
    password.addEventListener("keydown", submitOnEnter);
});


// update anything based on login