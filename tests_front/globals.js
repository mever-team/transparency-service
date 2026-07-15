let loadedJS = [];
const loadOnce = ['shellui.js', 'bearer.js']
async function loadPage(url, asAdmin=false){
    let thisToken = '';
    if (asAdmin) {
         await $.ajax({
            url: '/transparency/login',
            method: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({username: 'admin', password: 'admin'}),
            success: function (response) {
                document.cookie="access_token="+response.token+"; path=/;"
                thisToken = response.token;
            },
            error: function (xhr) {
                console.log('Failed to login as admin from Karma')
            }
        });
    }
    const response = await fetch(url, {headers: {'Authorization': `Bearer ${thisToken}`}});
    let html = await response.text();

    html = html.replaceAll(
        '"js/',
        '"/base/ui/transparency/js/'
    );
    html = html.replaceAll(
        "'js/",
        "'/base/ui/transparency/js/"
    );

    const doc = new DOMParser().parseFromString(html, 'text/html');

    document.body.innerHTML = doc.body.innerHTML;

    const scripts = [...doc.querySelectorAll('script')];
    for (const oldScript of scripts) {
        const script = document.createElement('script');

        script.async = false;

        if (oldScript.type) {
            script.type = oldScript.type;
        }

        if (oldScript.src) {
            script.src = oldScript.src;
            let skipJS = false;
            if(loadedJS.includes(script.src.replace(/\/$/, "").split("/").pop())){
                for( let once of loadOnce){
                    if (script.src.includes(once)){
                        skipJS = true;
                        continue;
                    }
                }
            }
            if (skipJS) {
                // console.log('skipping: ' + script.src);
                continue;
            }

            await new Promise((resolve, reject) => {
                script.onload = () => {
                    // console.log('loaded:', script.src);
                    loadedJS.push(script.src.replace(/\/$/, "").split("/").pop());
                    resolve();
                };

                script.onerror = (err) => {
                    console.log('FAILED:', script.src);
                    reject(err);
                };

                document.head.appendChild(script);
            });

        } else {
            // Inline script
            script.textContent = oldScript.textContent;
            document.head.appendChild(script);
        }
    }

    await new Promise(resolve => setTimeout(resolve, 5000));
}

async function createCard(username, password) {
    let token = '';
    // login
    await $.ajax({
        url: '/transparency/login',
        method: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({username: 'admin', password: 'admin'}),
        success: function (response) {
            token = response.token;
        },
        error: function (xhr) {
            console.log(`Failed to login as ${username} from Karma`)
        }
    });
    // create card
    let cardId = '';
    await $.ajax({
        url: "/transparency/card",
        method: "POST",
        contentType: "application/json",
        headers: { "Authorization": "Bearer " + token },
        data: JSON.stringify({ title: "" }),
        success: r => cardId = r,
        error: () => alert("Failed to create a new model card. Please refresh the page and try again.")
    });

    return cardId;
}