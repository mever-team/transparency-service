let quantitative_analysis_textarea_instance;
let considerations_textarea_instance;
let model_details_textarea_instance;
let training_set_textarea_instance;
let eval_set_textarea_instance;
let previous_field = '';
let fileInput;
let uploadBtn;


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

    let formData = { textarea: "", user_input: "", field: previous_field };
    const textAreas = document.querySelectorAll('#leftPane textarea');

    const textareaInstances = {
        "Submit from model details": { instance: model_details_textarea_instance, field: "Model Details" },
        "Add AI tips": {field: "Level of Details" },
        "Submit from aichat": { value: textAreas[2]?.value || "", field: "Considerations" },
        "Submit from considerations": { instance: considerations_textarea_instance, field: "Considerations" },
        "Considerations": { field: "Considerations" },
        "Submit from training set": { instance: training_set_textarea_instance, field: "Training Set" },
        "Training Set": { field: "Training Set" },
        "Submit from eval set": { instance: eval_set_textarea_instance, field: "Eval Set" },
        "Eval Set": { field: "Eval Set" },
        "Submit from quantitative analysis": { instance: quantitative_analysis_textarea_instance, field: "Quantitative Analysis" },
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
            formData.textarea = textareaInstances[buttonName].instance.getData();
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

        console.log(formData);
        if (ckeditorFields[formData.field]) {
            ClassicEditor.create(document.querySelector(ckeditorFields[formData.field]))
                .then(editor => {
                    if (formData.field.includes("Training Set")) training_set_textarea_instance = editor;
                    else if (formData.field.includes("Eval Set")) eval_set_textarea_instance = editor;
                    else if (formData.field.includes("Quantitative Analysis")) quantitative_analysis_textarea_instance = editor;
                    else if (formData.field.includes("Considerations")) considerations_textarea_instance = editor;
                    else if (formData.field.includes("Model Details")) model_details_textarea_instance = editor;
                })
                .catch(error => console.error('Error initializing CKEditor:', error));
        }
    })
    .catch(error => console.error('Error:', error));
});


