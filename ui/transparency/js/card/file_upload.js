var uploaded_file;
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
            if (progress >= 100)
                clearInterval(interval);
        }, 100);
    }

    async function pdf2html(pdf) {
        if (!pdf) return '';
        const arrayBuffer = await pdf.arrayBuffer();
        const pdfDoc = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        let fullText = "";
        for (let i = 1; i <= pdfDoc.numPages; i++) {
            const page = await pdfDoc.getPage(i);
            const content = await page.getTextContent();
            const items = content.items;
            const paragraphGap = 12; // tweak this
            const lineTolerance = 2;
            let lines = [];
            let currentLine = [];
            let lastY = null;
            let paragraphText = "<p>";
            let lastLineY = null;
            
            // Sort items top-to-bottom, left-to-right
            items.sort((a, b) => {
                const yDiff = b.transform[5] - a.transform[5];
                if (Math.abs(yDiff) > 2) return yDiff;
                return a.transform[4] - b.transform[4];
            });
            // Construct lines
            items.forEach(item => {
                const y = item.transform[5];
                if (lastY === null || Math.abs(y - lastY) < lineTolerance) {
                    currentLine.push(item.str);
                } else {
                    lines.push({ text: currentLine.join(" "), y: lastY });
                    currentLine = [item.str];
                }
                lastY = y;
            });
            if (currentLine.length) {
                lines.push({ text: currentLine.join(" "), y: lastY });
            }
            // construct paragraphs
            lines.forEach((line, idx) => {
                if (lastLineY !== null && Math.abs(lastLineY - line.y) > paragraphGap) {
                    paragraphText += "</p><p>";
                } else if (idx !== 0) {
                    paragraphText += " ";
                }
                paragraphText += line.text.trim();
                lastLineY = line.y;
            });
            fullText += paragraphText;
        }
        fullText = fullText.replace('<p>','<h1>').replace('</p>', '</h1>');
        return fullText;
    }

    $dropArea.on('dragover', function (e) {
        e.preventDefault();
        $dropArea.addClass('hover');
    });

    $dropArea.on('dragleave', function (e) {
        e.preventDefault();
        $dropArea.removeClass('hover');
    });

    $fileInput.on('change', async function () {
        var $this = this;
        displayFiles($this.files);

        if ($this.files.length > 0) {
            uploaded_file = await pdf2html($this.files[0]);
        }
    });

    $dropArea.on('drop', async function (e) {
        e.preventDefault();
        $dropArea.removeClass('hover');
        const files = e.originalEvent.dataTransfer.files;
        $fileInput[0].files = files;
        displayFiles(files);
        if (files.length > 0) {
            uploaded_file = await pdf2html(files[0]);
        }

    });
});
