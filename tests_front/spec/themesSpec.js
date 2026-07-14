describe('Testing themes...', function() {
    beforeAll(async function() {
        const response = await fetch('/base/ui/transparency/index.html');
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
    });
    // afterAll(function() {
    //     token = undefined;
    // });

    it('Testing light theme', function(){
        setTheme('light-theme');
        expect(localStorage.getItem('theme')).toBe('light-theme');
        
    });

    it('Testing dark theme', function(){
        setTheme('dark-theme');
        expect(localStorage.getItem('theme')).toBe('dark-theme');
    });

    it('Testing ocean theme', function(){
        setTheme('ocean-theme');
        expect(localStorage.getItem('theme')).toBe('ocean-theme');
    });

})