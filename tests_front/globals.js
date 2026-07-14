let loadedJS = [];
const loadOnce = ['shellui.js', 'bearer.js']
async function loadPage(url){
    const response = await fetch(url);
    let html = await response.text();

    html = html.replaceAll(
        'js/',
        '/base/ui/transparency/js/'
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
            if(loadedJS.includes(script.src)){
                for( let once of loadOnce){
                    if (script.src.includes(once)){
                        skipJS = true;
                        continue;
                    }
                }
            }
            if (skipJS) continue;

            await new Promise((resolve, reject) => {
                script.onload = () => {
                    // console.log('loaded:', script.src);
                    loadedJS.push(script.src);
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