$(document).ready(function () {
    const $dropArea = $('#dropArea');
    const $fileInput = $('.file-input');
    const $fileList = $('#fileList');
    const $totalSize = $('#totalSize');
    const $progressFill = $('#progressFill');

    function getIconForFile(file) {
        const ext = file.name.split('.').pop().toLowerCase();
        if (['jpg', 'jpeg', 'png'].includes(ext)) return '🖼️';
        if (ext === 'pdf') return '📄';
        return '📁';
    }

    function formatSize(bytes) {
        return (bytes / 1024).toFixed(1) + ' KB';
    }

    function displayFiles(files) {
        $fileList.empty();
        let totalBytes = 0;

        for (const file of files) {
            const icon = getIconForFile(file);
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

            if (progress >= 100) {
                clearInterval(interval);
            }
        }, 100);
    }

    $fileInput.on('change', function () {
        var $this = this
        displayFiles($this.files);
        // upload the first file (or loop if multiple allowed)
        if ($this.files.length > 0) {
            setTimeout(function () {
                uploadFile($this.files[0]);
            }, 1300)
        }
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
        const files = e.originalEvent.dataTransfer.files;
        $fileInput[0].files = files;
        displayFiles(files);
        if (files.length > 0) {
            setTimeout(function () {
                uploadFile(files[0]);
            }, 1300)
        }
    });
});
