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
            data: JSON.stringify({ query: q, type: typeFilters, task: taskFilters }),
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
                            <tr class="search_results_button" onclick="toggleExtraContent(this);">
                                <td>
                                    <div>
                                    <svg class="quality-circle" viewBox="0 0 36 36">
                                        <circle cx="18" cy="18" r="18" fill="none" stroke="#434343" stroke-width="3"/>
                                        <circle cx="18" cy="18" r="18" fill="none" stroke="${it.quality>0.7?'#6CC06B':it.quality>0.4?'#FBC483':'#F87F76'}" stroke-width="3"
                                        stroke-dasharray="100" stroke-dashoffset="${100 - Math.round(it.quality * 100)}"/>
                                        <text x="18" y="14" class="quality-text"> ${Math.round(it.quality * 100)}%</text>
                                        <text x="18" y="24" class="quality-text">info</text>
                                    </svg>
                                    </div>
                                </td>
                                <td>${name}</td>
                                <td>${it.task || '-'}</td>
                                <td>${it.type || '-'}</td>
                            </tr>

                            <tr class="results_extra_content">
                                <td>
                                    <div class="extra_content">
                                        <div class="extra_content_inner">
                                            <p>
                                                ${it.overview}
                                            </p>
                                            <p>
                                                Date of production: <input type="date" readonly value="${it.date}" class="inline-date">
                                            </p>

                                            <button class="open-card-btn" onclick="window.location='model_card.html?id=${it.id}'"> Open Card</button>
                                        </div>
                                    </div>
                                </td>
                            </tr>

                            `);
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

    $("#typeFilters").on('click',  () => {
        lastUpdate = Date.now();
        request();
    });
    $("#taskFilters").on('click',  () => {
        lastUpdate = Date.now();
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


function toggleExtraContent(buttonRow) {
    const extraContent = buttonRow.nextElementSibling.querySelector('.extra_content');
    const innerContent = buttonRow.nextElementSibling.querySelector('.extra_content_inner');

    if (extraContent.classList.contains('open')) {
        extraContent.classList.remove('open');
        extraContent.style.maxHeight = '0';
    } else {
        const contentHeight = innerContent.scrollHeight;
        extraContent.style.maxHeight = contentHeight + 20 + 'px';
        extraContent.classList.add('open');
    }
}


fetch('/transparency/options/overview/task')
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById("taskFilters");
        const cancelAll = document.createElement("span");
        cancelAll.textContent = '❌ Remove All Filters'
        cancelAll.classList.add("filter-cancel");
        cancelAll.id = 'taskFiltersCancel';
        container.appendChild(cancelAll);

        data.forEach(taskOption => {
            const span = document.createElement("span");
            if (taskOption.startsWith("#")) {
                span.textContent = taskOption.replace("#", "");
                span.classList.add("filter-optgroup");
            }
            else{
                span.textContent = taskOption;
                span.classList.add("filter-option");
                span.id = taskOption;
            }
            container.appendChild(span);
        });
    })
    .catch(err => {
        console.error(err);
});


let taskFilters = [];
let typeFilters = [];
fetch('/transparency/options/overview/type')
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById("typeFilters");
        const cancelAll = document.createElement("span");
        cancelAll.textContent = '❌ Remove All Filters'
        cancelAll.classList.add("filter-cancel");
        cancelAll.id = 'typeFiltersCancel';
        container.appendChild(cancelAll);

        data.forEach(taskOption => {
            const span = document.createElement("span");
            if (taskOption.startsWith("#")) {
                span.textContent = taskOption.replace("#", "");
                span.classList.add("filter-optgroup");
            }
            else{
                span.textContent = taskOption;
                span.classList.add("filter-option");
                span.id = taskOption;
            }
            container.appendChild(span);
        });

    })
    .catch(err => {
        console.error(err);
});


document.addEventListener("click", (e) => {
    const filters = document.getElementById("taskFilters");
    const toggle = document.getElementById("taskFiltersBtn");

    if (!filters.contains(e.target) && !toggle.contains(e.target)) {
        filters.classList.add("hidden");
    }
});

document.addEventListener("click", (e) => {
    const filters = document.getElementById("typeFilters");
    const toggle = document.getElementById("typeFiltersBtn");

    if (!filters.contains(e.target) && !toggle.contains(e.target)) {
        filters.classList.add("hidden");
    }
});

document.getElementById("taskFilters").addEventListener("click", (e) => {
    if (!e.target.id) return;
    if (e.target.id.includes("Cancel")) {
        taskFilters = [];
        document.getElementById("taskFiltersBtn").classList.remove("active");
        const children = Array.from(document.getElementById("taskFilters").children);
        children.forEach(child => child.classList.remove("active"));
        autocomplete_populate();
        return;
    }
    if(taskFilters.includes(e.target.id)){
        taskFilters.splice(taskFilters.indexOf(e.target.id), 1);
    }
    else {
        taskFilters.push(e.target.id);
    }
    document.getElementById(e.target.id).classList.toggle("active");

    if (taskFilters.length > 0) {
        document.getElementById("taskFiltersBtn").classList.add("active");
    }
    else
    {
        document.getElementById("taskFiltersBtn").classList.remove("active");
    }
    autocomplete_populate();
});


document.getElementById("typeFilters").addEventListener("click", (e) => {
    if (!e.target.id) return;
    if (e.target.id.includes("Cancel")) {
        typeFilters = [];
        document.getElementById("typeFiltersBtn").classList.remove("active");
        const children = Array.from(document.getElementById("typeFilters").children);
        children.forEach(child => child.classList.remove("active"));
        return;
    }
    if(typeFilters.includes(e.target.id)){
        typeFilters.splice(typeFilters.indexOf(e.target.id), 1);
    }
    else {
        typeFilters.push(e.target.id);
    }
    document.getElementById(e.target.id).classList.toggle("active");

    if (typeFilters.length > 0) {
        document.getElementById("typeFiltersBtn").classList.add("active");
    }
    else
    {
        document.getElementById("typeFiltersBtn").classList.remove("active");
    }
});