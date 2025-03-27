function showTabContent(tabId) {
    // Select all elements with the class 'tab-content'
    const contents = document.querySelectorAll('.tab-content');
    // Loop through each content element and remove the 'active-content' class
    contents.forEach(content => content.classList.remove('active-content'));

    // Select all elements with the class 'tab'
    const tabs = document.querySelectorAll('.tab');
    // Loop through each tab element and remove the 'active-tab' class
    tabs.forEach(tab => tab.classList.remove('active-tab'));

    // Find the specific tab content by its ID and add the 'active-content' class
    document.getElementById(tabId).classList.add('active-content');

    // Find the currently active tab by matching the onclick attribute with the given tabId
    const activeTab = document.querySelector('.tab[onclick="showTabContent(\'' + tabId + '\')"]');
    // Add the 'active-tab' class to the currently active tab
    activeTab.classList.add('active-tab');
}

function toggleShowMoreContent(button) {
    const content = button.nextElementSibling;
    if (content.style.display === "none") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
}