$(function () {
    let chartInstance = null;

    function update_resources(response) {
        const $pending = $("#pending-users").empty();
        if (response.pending.length === 0) $pending.hide();
        else {
            $registered.append("<h2>Pending approval (did not register via email)</h2>");
            response.pending.forEach(u => {$pending.append(`
                <div class="user">
                    <span style="username">${u.username}</span> - ${u.email || "no contact info"}
                    <span class="delete-btn error button" data-username="${u.username}"><i class="fa-solid fa-cancel"></i>&nbsp;Reject</span>
                    <span class="pending-btn warning button" data-username="${u.username}"><i class="fa-solid fa-key"></i>&nbsp;Accept</span>
                </div>
            `);});
        }
        const $registered = $("#registered-users").empty();
        if (response.users.length === 0) $registered.hide();
        else {
            if(response.users.length>1) $registered.append("<h2>Registered users</h2>");
            else $registered.append("<h2>Your account</h2>");
            response.users.forEach(u => { $registered.append(`
                <div class="user">
                    <span class="username">${u.username}</span> - ${u.email||"no contact info"}
                    <span class="delete-btn error button" data-username="${u.username}"><i class="fa-solid fa-trash"></i>&nbsp;Delete</span>
                    <span class="registered-label">Registered</span>
                </div>
            `);});
        }
        const $cards = $("#cards").empty();
        if (!response.cards || response.cards.length === 0) $cards.hide();
        else {
            $cards.append("<h2>Your cards at a glance</h2>");
            response.cards.forEach((card, i) => {$cards.append(`
                <div class="card" data-card="${card.id}">
                    <span class="counter">${i + 1}.</span>&nbsp;<span class="username"><a href="/transparency/model_card.html?id=${card.id}">${card.name}&nbsp;</a></span>`
                +(card.working?`<span>An agent is working on this</span>`:`<span class="card-delete-btn error button" data-card="${card.id}"><i class="fa-solid fa-trash"></i>&nbsp;Delete</span>`)
                +(card.desc?`<span class="unpublish-btn warning button" data-card="${card.id}"><i class="fa-solid fa-undo"></i>&nbsp;Unpublish: ${card.desc}</span>`:"<span class='placeholder'>[DRAFT]</span>")
                +(loggedUserIsAdmin&&card.report_count?`<span class="resolve-btn success button" data-card="${card.id}"><i class="fa-solid fa-check"></i>&nbsp;Close reports</span>`:"")
                +(card.report_count?`<span class="show-reports-btn error button" data-card="${card.id}" data-cardname="${card.name+' '+card.desc}">${card.report_count} reports</span>`:"")
                +`</div>
            `);});
        }
        const $reported = $("#reported").empty();
        if (!response.reported || response.reported.length === 0) $reported.hide();
        else {
            $reported.append("<h2>Reported cards from other users</h2>");
            response.reported.forEach(card => {$reported.append(`
                <div class="card" data-card="${card.id}">
                    <span class="username"><a href="/transparency/model_card.html?id=${card.id}">${card.name}&nbsp;</a></span>
                `
                +(card.working?`<span>An agent is working on this</span>`:`<span class="card-delete-btn error button" data-card="${card.id}"><i class="fa-solid fa-trash"></i>&nbsp;Delete</span>`)

                +(card.desc?`<span class="unpublish-btn warning button" data-card="${card.id}"><i class="fa-solid fa-undo"></i>&nbsp;Unpublish: ${card.desc}</span>`:"<span class='placeholder'>DRAFT</span>")
                +(loggedUserIsAdmin&&card.report_count?`<span class="resolve-btn success button" data-card="${card.id}"><i class="fa-solid fa-check"></i>&nbsp;Close reports</span>`:"")
                +(card.report_count?`<span class="show-reports-btn error button" data-card="${card.id}" data-cardname="${card.name+' '+card.desc}">${card.report_count} reports</span>`:"")
                +`</div>
            `);});
        }
        const $resources = $("#resources");
        if (response.resources) {
            $resources.show();
            const r = response.resources;
            const labels = r.cpu.map((_, i) => i);
            if (chartInstance) {
                chartInstance.data.labels = labels;
                chartInstance.data.datasets[0].data = r.cpu;
                chartInstance.data.datasets[1].data = r.ram;
                chartInstance.data.datasets[2].data = r.disk;
                chartInstance.update();
            } else {
                $resources.append('<canvas id="metrics-chart" style="max-height: 300px;"></canvas>');
                chartInstance = new Chart(document.getElementById('metrics-chart'), {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'CPU %',
                                data: r.cpu,
                                borderColor: 'firebrick',
                                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                                fill: true,
                                tension: 0.3
                            },
                            {
                                label: 'RAM %',
                                data: r.ram,
                                borderColor: 'royalblue',
                                backgroundColor: 'rgba(65, 105, 225, 0.1)',
                                fill: true,
                                tension: 0.3
                            },
                            {
                                label: 'Disk %',
                                data: r.disk,
                                borderColor: 'orange',
                                backgroundColor: 'rgba(255, 165, 0, 0.1)',
                                fill: true,
                                tension: 0.3
                            }
                        ]
                    },
                    options: {
                        animation: false,
                        plugins: { title: { display: true, text: 'System resources (worst value per minute of uptime, total RAM: ' + r.ram_total_gb + ' GB)' } },
                        scales: { y: { min: 0, max: 100 } }
                    }
                });
            }
        } else {
            $resources.hide();
            if (chartInstance) {
                chartInstance.destroy();
                chartInstance = null;
            }
        }

        $(".is-admin").show();
        $('#loading').hide();
    }

    function fetchData() {
        $.ajax({
            url: "/transparency/users",
            contentType: "application/json",
            dataType: "json",
            headers: {"Authorization": "Bearer " + token},
            success: update_resources,
            error: {}
        });
    }

    $('#logout-btn').click(() => { token = ""; document.cookie = "access_token=; path=/; max-age=0;"; window.location.href = 'index.html'; });
    $('#loading').show();

    fetchData(); // Initial fetch

    // Poll every 60 seconds if resources exist
    setInterval(fetchData, 60000);

    $(document).on('click', '.pending-btn', function () {
        const username = $(this).data('username');
        $.ajax({
            url: `/transparency/users/${username}/accept`,
            method: "POST",
            headers: { "Authorization": "Bearer " + token },
            success: function () {
                location.reload();
            },
            error: function (xhr) {
                alert(xhr.responseJSON?.error || "Failed to accept user");
            }
        });
    });
    $(document).on('click', '.delete-btn', function () {
        const username = $(this).data('username');
        if(username === loggedUser) {
            if (!confirm(`Delete your account? This will remove all your data, including created model cards, and cannot be undone.`)) return;
        }
        else if(!confirm(`Remove user "${username}"? This will remove all their data, including model cards, and cannot be undone?`)) return;
        $.ajax({
            url: `/transparency/users/${username}`,
            method: "DELETE",
            headers: { "Authorization": "Bearer " + token },
            success: function () {
            if(username === loggedUser) {
                token = "";
                document.cookie = "access_token=; path=/; max-age=0;";
                window.location.href = "index.html";
            }
            else  location.reload();
        },
            error: xhr => alert(xhr.responseJSON?.error || "Failed to delete user")
        });
    });
    $(document).on('click', '.card-delete-btn', function () {
        const card_id = $(this).data('card');
        $.ajax({
            url: `/transparency/card/${card_id}`,
            method: "DELETE",
            headers: { "Authorization": "Bearer " + token },
            success: function () {location.reload();},
            error: xhr => alert(xhr.responseJSON?.error || "Failed to delete card")
        });
    });
    $(document).on('click', '.unpublish-btn', function () {
        const card_id = $(this).data('card');
        $.ajax({
            url: `/transparency/card/${card_id}/overview/version`,
            method: "PUT",
            contentType: "application/json",
            data: JSON.stringify({value: "", message: "Unpublished"}),
            headers: { "Authorization": "Bearer " + token },
            success: function () {location.reload();},
            error: xhr => alert(xhr.responseJSON?.error || "Failed to unpublish card")
        });
    });
    $(document).on('click', '.show-reports-btn', function () {
        const card_id = $(this).data('card');
        const card_name = $(this).data('cardname');
        $.ajax({
            url: `/transparency/reports/${card_id}`,
            method: "GET",
            contentType: "application/json",
            data: JSON.stringify({value: "", message: "unpublished"}),
            headers: { "Authorization": "Bearer " + token },
            success: function (reports) {
                //console.log(reports);
                $('#report-card-name').text(card_name);
                const $list = $('#report-list').empty();
                reports.forEach(r => $list.append(`<div class="report-entry">${r}</div>`));
                document.getElementById('report-modal-screen').style.display = 'flex';
            },
            error: xhr => alert(xhr.responseJSON?.error || "Failed to obtain a list of reports")
        });
    });
    $(document).on('click', '.resolve-btn', function () {
        const card_id = $(this).data('card');
        $.ajax({
            url: `/transparency/reports/${card_id}`,
            method: "DELETE",
            headers: { "Authorization": "Bearer " + token },
            success: function () {location.reload();},
            error: xhr => alert(xhr.responseJSON?.error || "Failed to resolve card reports")
        });
    });
    $('#password-open-btn').click(()=>{
        document.getElementById('password-modal-screen').style.display = 'flex';
    });
    $('#cancel-password-btn').click(()=>{
        document.getElementById('password-modal-screen').style.display = 'none';
        $('#password-error').text("");
    });
    $('#cancel-report-btn').click(()=>{
        document.getElementById('report-modal-screen').style.display = 'none';
    });
    $('#confirm-password-btn').click(function(){
        const password=$("#password").val();
        const verify=$("#password-verify").val();
        if(!password) {
            $('#password-error').text("Provide a new password.");
            return;
        }
        if(password!==verify) {
            $('#password-error').text("The new password does not match its verification.");
            return;
        }
        $.ajax({
            url: "/transparency/update_password",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({password:password}),
            headers: {"Authorization":"Bearer "+token},
            success: function(res){
                token=res.token;
                document.cookie="access_token="+res.token+"; path=/;";
                $('#password-modal-screen').fadeOut(150);
                $("#password").val("");
                $("#password-verify").val("");
                document.getElementById('password-modal-screen').style.display = 'none';
            },
            error: function(xhr){
                $('#password-error').text(xhr.responseJSON?.error||"Failed to set new password.");
            }
        });
    });


    $(document).on('click', '.close-modal, #report-modal-screen', function (e) {
        if (e.target.id === 'report-modal-screen' || $(e.target).hasClass('close‑modal'))
            document.getElementById('report-modal-screen').style.display = 'none';
    });

    theme = localStorage.getItem("theme") || 'light-theme';
    $('#theme-selector').val(theme);
    $('#theme-selector').on('change', function (e) {
        var optionSelected = $("option:selected", this);
        var valueSelected = this.value;
        localStorage.setItem("theme", valueSelected);
        theme = valueSelected;
        setTheme(theme);
    });
});
