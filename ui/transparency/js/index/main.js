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
            url: "/transparency/card",
            method: "POST",
            contentType: "application/json",
            headers: { "Authorization": "Bearer " + token },
            data: JSON.stringify({ title: "" }),
            success: r => window.location.href = 'model_card.html?id=' + r,
            error: () => alert("Failed to create a new model card. Please refresh the page and try again.")
        });
    });

    $(document).on('click', '.dropdown-btn', function(e) {
        e.stopPropagation();
        $(this).parent().toggleClass('show');
    });

    $(document).on('click', function() {
        $('.dropdown-filter').removeClass('show');
    });

});

function autocomplete_populate() {
    let lastUpdate = 0, pending = null, first = true, delay = 150;
    const $topic = $("#topic"), $tbody = $("#resultsTable tbody");

    function request() {
        const q = $topic.val().trim();
        if (first) $('#loading').show();
        $.ajax({
            url: "/transparency/cards",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ query: q }),
            success: r => {
                $('#loading').hide();
                const results = r.results || [];
                $('#search_results_wrapper').text(q ? "Showing" : "Showing");
                $('#search_results').text(results.length + " of " + (r.total || 0));
                $tbody.empty();
                if (results.length)
                    results.forEach(it => {
                        const name = it.name.replace(new RegExp("(" + q + ")", "ig"), "<strong style='color:#79CFDC'>$1</strong>");
                        $tbody.append(`
                            <tr class="search_results_button">
                                <td><a style="display:block;width:100%;height:100%;text-decoration:none" href="model_card.html?id=${it.id}">
                                    <div class="row">
                                      <div>
                                        <svg class="quality-circle" viewBox="0 0 36 36">
                                          <circle cx="18" cy="18" r="18" fill="none" stroke="#434343" stroke-width="3"/>
                                          <circle cx="18" cy="18" r="18" fill="none" stroke="${it.quality>0.7?'6CC060B':it.quality>0.4?'#FBC483':'#F87F76'}" stroke-width="3"
                                            stroke-dasharray="100" stroke-dashoffset="${100 - Math.round(it.quality * 100)}"/>
                                          <text x="18" y="14" class="quality-text"> ${Math.round(it.quality * 100)}%</text>
                                          <text x="18" y="24" class="quality-text">info</text>
                                        </svg>
                                      </div>
                                      <div>
                                        <span style="display:block;color:#EEE">${name}</span>
                                        <span style="font-size:13px;color:#F9AB49">
                                          ${it.desc ? "" : "DRAFT (no version)"}
                                        </span>
                                        <span style="font-size:13px;color:#79CFDC"> ${it.desc + " by " + it.creator || ""} </span>
                                      </div>
                                    </div>
                                    <div style="font-size:13px;color:#C8C8C8;margin-top:7px">${it.overview || ""}</div>
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

    $(document).on('click', '.dropdown-content a', function (e) {
        e.preventDefault();
        const text = $(this).children().first().text().trim().toLowerCase();
        const tag = `${text}`;
        const $input = $('#topic');
        const currentVal = $input.val();

        // Only add tag if not already present
        if (!currentVal.includes(tag)) {
            $input.val(currentVal + (currentVal ? ' ' : '') + tag + ' ');
        }

        $input.focus();
        lastUpdate = Date.now();
        request();
    });

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
        url: "/transparency/login",
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
