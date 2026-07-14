let loaded = [];
describe('Testing filters...', function() {
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
                        loadedJS.push(script.src);
                        resolve();
                    };

                    script.onerror = (err) => {
                        // console.log('FAILED:', script.src);
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
    //     console.log('token');
    //     console.log(token);
    //     token = undefined;
    //     console.log(token);
    // });

    it('Set & remove a Task filter', function() {
        /* Open filter modal */
        $("#new-filter").trigger('click');
        $modal = $(".modal.modal__bg#filters");
        expect($modal.hasClass('modal--active')).toBe(true);

        /* Select a 'Task' filter */
        document.getElementById('filter-select').value = 'task';
        document.getElementById('filter-select').dispatchEvent(new Event("change", { bubbles: true }));
        $('.filter-option[data-filter="Audio-Text-to-Text"]').trigger('click');
        expect($('.filter-option[data-filter="Audio-Text-to-Text"]').hasClass('active')).toBe(true);

        /* Trigger done and check caption */
        $('.filter-done').trigger('click');
        $taskFilterCaption = $('#edit-filter[data-filter="task"]');
        expect($taskFilterCaption.html()).toContain('Audio‑Text‑to‑Text');

        /* Edit filter */
        $taskFilterCaption.trigger('click');
        $modal = $(".modal.modal__bg#filters");
        expect($modal.hasClass('modal--active')).toBe(true);
        $('.filter-option[data-filter="Image-Text-to-Text"]').trigger('click');
        $('.filter-done').trigger('click');
        $taskFilterCaption = $('#edit-filter[data-filter="task"]');
        expect($taskFilterCaption.html()).toContain('Image‑Text‑to‑Text');

        /* Remove Task filter and check caption */
        $taskFilterCaption.find('.remove-filter').trigger('click');
        $taskFilterCaption = $('#edit-filter[data-filter="task"]');
        expect($taskFilterCaption.html()).toBe(undefined);
    });
});