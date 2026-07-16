describe('Testing eval_adapter.js...', function() {
    let fakeMetrics;
    let fakeFile

    beforeAll(async function () {
        fakeMetrics = {"package_version": "0.1.0",  "date": "2025-Nov-14",  "task": "Text Classification",  "energy_consumption": "0.638 Wh", "metrics": {  "precision_macro": 0.509,  "precision_micro": 0.574,  "recall_macro": 0.464,  "recall_micro": 0.574,  "top1_acc_micro": 0.574,  "top1_acc_macro": 0.574,  "top1_acc_weighted": 0.574,  "f1_macro": 0.466,  "f1_micro": 0.574,  "auc_roc_macro": 0.928,  "auc_roc_weighted": 0.909},  "batch_size": 32,  "hardware": "CPU: AMD Ryzen 7 7800X3D 8-Core Processor, RAM: 15.62 GB, CUDA: | NVIDIA-SMI 580.102.01 Driver Version: 581.57 CUDA Version: 13.0|",  "execution_time": "inference: 34.68s, metrics: 45.76ms",  "num_classes": 28}
        fakeFile = new File( 
            [JSON.stringify(fakeMetrics, null, 2)],
            "metrics.json",
            { type: "application/json" }
        );
        karmaTestCardId = await createCard('admin', 'admin');
        let url = '/base/ui/transparency/model_card.html';
        await loadPage(url, asAdmin = true);
    });
    afterAll(function(){
        $(document).off("click", ".card-button");
    });

    it('Sending request', async function(){
        /* Fake a drop file event */
        expect($('#progressFillMetrics')[0].outerHTML.includes('width: 100%;')).toBe(false);
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(fakeFile);
        const dropEvent = new DragEvent('drop', {
            bubbles: true,
            cancelable: true,
            dataTransfer: dataTransfer
        });
        $('#dropAreaMetrics')[0].dispatchEvent(dropEvent);
        await new Promise(resolve => setTimeout(resolve, 2000)); // wait for fake slide to fill
        expect($('#progressFillMetrics')[0].outerHTML.includes('width: 100%;')).toBe(true);

        /* make the request */
        
    });

})