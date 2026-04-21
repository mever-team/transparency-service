$(function () {
    var uploaded_metrics;
    const $modal = $('#metrics-container');
    const $dropArea = $modal.find('#dropAreaMetrics');
    const $fileInput = $modal.find('.file-input');
    const $fileList = $modal.find('#fileListMetrics');
    const $totalSize = $modal.find('#totalSizeMetrics');
    const $progressFill = $modal.find('#progressFillMetrics');
    $(document).on('click', '.card-button#agent[data-type="metrics"]', request);

    function request (){
        const urlParams = new URLSearchParams(window.location.search);
        const id = urlParams.get('id');
        if (!uploaded_metrics) return
        $.ajax({
            url: "/transparency/eval_adapter/" + id,
            type: "POST",
            contentType: "application/json",
            headers: {"Authorization": "Bearer " + token},
            data: JSON.stringify(uploaded_metrics),
            success: function(response) {
                window.location.href = window.location.href;
            },
            error: function(xhr, status, error) {
                $modal.css('display','none');
                error_handler(xhr, status, error);
            }
        });
    }

    function openMetricsModal () {
        $modal.css('display','flex');
    }

    function formatSize(bytes) {
        return (bytes / 1024).toFixed(1) + ' KB';
    }

    function displayFiles(files) {
        $fileList.empty();
        let totalBytes = 0;
        for (const file of files) {
            const icon = '📄';
            totalBytes += file.size;
            $fileList.append(`<li><span class="icon">${icon}</span> ${file.name} — ${formatSize(file.size)}</li>`);
        }
        $totalSize.text('Total size: ' + formatSize(totalBytes));
        simulateUploadProgress();
    }

    function simulateUploadProgress() {
        let progress = 0;
        $progressFill.width('0%');
        const interval = setInterval(() => {
            progress += 10;
            $progressFill.width(progress + '%');
            if (progress >= 100)
                clearInterval(interval);
        }, 10);
    }

    $fileInput.on('change', function () {
        const file = this.files[0];
        if (!file) return;
        displayFiles([file]);
        file.text().then(text => {
            try {
                uploaded_metrics = JSON.parse(text);
            } catch (err) {
                console.error("Invalid JSON file:", err);
            }
        });
    });


    $dropArea.on('dragover', function (e) {
        e.preventDefault();
        $dropArea.addClass('hover');
    });

    $dropArea.on('dragleave', function (e) {
        e.preventDefault();
        $dropArea.removeClass('hover');
    });

    $dropArea.on('drop', function (e) {
        e.preventDefault();
        $dropArea.removeClass('hover');
        const file = e.originalEvent.dataTransfer.files[0];
        if (!file) return;
        $fileInput[0].files = e.originalEvent.dataTransfer.files;
        displayFiles([file]);
        file.text().then(text => {
            try {
                uploaded_metrics = JSON.parse(text);
            } catch (err) {
                console.error("Invalid JSON file:", err);
            }
        });
    });
})