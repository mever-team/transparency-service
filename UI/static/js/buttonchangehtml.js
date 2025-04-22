let quantitative_analysis_textarea_instance;
let considerations_textarea_instance;
let model_details_textarea_instance;
let training_set_textarea_instance;
let eval_set_textarea_instance;
let previous_field = '';
let fileInput;
let uploadBtn;
let editorInstances = {};

// Function to change content in both left and right panes
function changePaneContent(leftHtml, rightHtml) {
    const leftPane = document.getElementById('leftPane');
    const rightPane = document.getElementById('rightPane');

    // Update the left and right panes with new HTML content
    leftPane.innerHTML = leftHtml;
    rightPane.innerHTML = rightHtml;


    executeScripts(leftHtml);
    executeScripts(rightHtml);
}

// Function to extract and execute JavaScript from HTML content
function executeScripts(html) {
    if (html)
    {
    const scripts = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g);
    if (scripts) {
        scripts.forEach(script => {
            const scriptContent = script.replace(/<script[^>]*>/, '').replace(/<\/script>/, '');
            const newScript = document.createElement('script');
            newScript.textContent = scriptContent;
            document.body.appendChild(newScript);  // Appending script to the body executes it
        });
    }
    }
}



document.addEventListener('click', function(event) {
    const button = event.target.closest('.dynamic-btn');
    if (!button) return;

    const buttonName = button.getAttribute('data-button-name');
    console.log("Button clicked, name:", buttonName);

    let formData = { textarea: {}, user_input: "", field: previous_field };
    const textAreas = document.querySelectorAll('#leftPane textarea');

    const textareaInstances = {
        //"Submit from model details": { instance: model_details_textarea_instance, field: "Model Details" },
        "Submit from model details": { instance: editorInstances, field: "Model Details" },
        "Add AI tips": {field: "Level of Details" },
        "Submit from aichat": { value: textAreas[2]?.value || "", field: "Considerations" },
        "Submit from considerations": { instance: editorInstances, field: "Considerations" },
        "Considerations": { field: "Considerations" },
        "Submit from training set": { instance: editorInstances, field: "Training Set" },
        "Training Set": { field: "Training Set" },
        "Submit from eval set": { instance: editorInstances, field: "Eval Set" },
        "Eval Set": { field: "Eval Set" },
        "Submit from quantitative analysis": { instance: editorInstances, field: "Quantitative Analysis" },
        "Quantitative Analysis": { field: "Quantitative Analysis" },
        "AI Data Summary Train Set": { field: "Training Set" },
        "AI Data Summary Eval Set": { field: "Eval Set" },
        "Upload PDF": { field: "Model Details" },
        "Model Details": { field: "Model Details" },
        "Level of Details": { field: "Level of Details" },
        "Upload Metrics": {field: "Quantitative Analysis"},
        "Add Tip": {value: textAreas[0]?.value + '<term_divider_tip>' + textAreas[1]?.value, field: "Level of Details"},
        "Create Level of Details": {field: "Level of Details"}
    };

    if (textareaInstances[buttonName]) {
        if (textareaInstances[buttonName].instance) {
            for (let key in textareaInstances[buttonName].instance)
            {
                formData.textarea[key] = textareaInstances[buttonName].instance[key].getData();
            }
        } else if (textareaInstances[buttonName].value) {
            formData.user_input = textareaInstances[buttonName].value;
        }
        formData.field = textareaInstances[buttonName].field;
    }

    previous_field = formData.field;
    console.log(formData);

    const bodyData = { button: buttonName };
    if (Object.keys(formData).length > 0) {
        bodyData.formData = formData;
    }

    fetch('/change_templates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyData)
    })
    .then(response => response.json())
    .then(data => {
        changePaneContent(data.new_left_html, data.new_right_html);

        const ckeditorFields = {
            "Quantitative Analysis": "#quantitative_analysis",
            "Upload Metrics": "#quantitative_analysis",
            "Considerations": "#considerations",
            "Model Details": "#model_details",
            "Training Set": "#training_set",
            "AI Data Summary Train Set": "#training_set",
            "Eval Set": "#eval_set",
            "AI Data Summary Eval Set": "#eval_set"
        };

        const lefttitle = new DOMParser().parseFromString(data.new_left_html, 'text/html').querySelector('title')?.textContent || "";

        if (lefttitle !== "Level of Details Editor"){

        document.querySelectorAll("textarea").forEach(textarea => {
            const skipIds = ["airesponse", "textInput"];

            if (skipIds.includes(textarea.id)) {
                return; // skip this textarea
            }
            ClassicEditor
                .create(textarea)
                .then(editor => {
                    editorInstances[textarea.id] = editor;

                    // only show toolbar if focused
                    const toolbar = editor.ui.view.toolbar.element;
                    toolbar.style.display = "none";
                    editor.editing.view.document.on('focus', () => {toolbar.style.display = "";});
                    editor.editing.view.document.on('blur', () => {toolbar.style.display = "none";});
                })
                .catch(error => {
                    console.error("Editor initialization failed for textarea:", textarea, error);
                });
        });
        }
    })
    .catch(error => console.error('Error:', error));
});


