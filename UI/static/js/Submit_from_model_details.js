document.addEventListener('click', function(event) {
    const button = event.target.closest('.dynamic-btn');
    if (!button) return;

    const buttonName = button.getAttribute('data-button-name');
    console.log("Button clicked, name:", buttonName);

    // Collect form data only for the submit button
    let formData = {};
    if (buttonName === "Submit from model details") {
        const textAreas = document.querySelectorAll('#leftPane textarea');
        formData = {
            name: textAreas[0].value,
            overview: textAreas[1].value,
            version: textAreas[2].value,
            license: textAreas[3].value,
            github: textAreas[4].value,
            paper: textAreas[5].value
        };
    }

    // Include formData in the request body if collected
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
    })
    .catch(error => console.error('Error:', error));
});





