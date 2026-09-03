import time
import json


def test_import_url(client, admin_token, admin_card_id):
    for agent in ["matcher", "ollama"]:
        url = 'http://localhost:5000'
        card_id = admin_card_id
        # 1. start assistant process
        response = client.post(
            f"/transparency/assistant/{agent}/complete/{card_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"type": "url", "payload": url},
        )
        assert response.status_code == 200
        # 2. poll until finish
        time.sleep(1) # Give time to start
        timeout = 300
        start = time.time()
        while True:
            response = client.get(f"/transparency/card/{card_id}/locked", headers={"Authorization": f"Bearer {admin_token}"})
            data = response.get_json()
            if not data:
                break
            if time.time() - start > timeout:
                raise AssertionError(f"Assistant did not finish in time of pytest timeout: {timeout} secs")
            time.sleep(0.5)
        assert response.status_code == 200
    
    
def test_refine(client, admin_token, admin_card_id):
    for agent in ["ollama"]:
        card_id = admin_card_id
        # 2. start refine
        response = client.post(
            f"/transparency/assistant/{agent}/refine/{card_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        # 3. poll until finish
        time.sleep(2) # Give time for Ollama
        timeout = 300
        start = time.time()
        while True:
            response = client.get(f"/transparency/job/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
            data = response.get_json()
            if not data:
                break
            if time.time() - start > timeout:
                raise AssertionError(f"Assistant did not finish in time of pytest timeout: {timeout} secs")
            time.sleep(0.5)
        assert response.status_code == 200
    
def test_import_metrics(client, admin_token, admin_card_id):
    metrics = {"package_version": "0.1.0",  "date": "2025-Nov-14",  "task": "Text Classification",  "energy_consumption": "0.638 Wh", "metrics": {  "precision_macro": 0.509,  "precision_micro": 0.574,  "recall_macro": 0.464,  "recall_micro": 0.574,  "top1_acc_micro": 0.574,  "top1_acc_macro": 0.574,  "top1_acc_weighted": 0.574,  "f1_macro": 0.466,  "f1_micro": 0.574,  "auc_roc_macro": 0.928,  "auc_roc_weighted": 0.909},  "batch_size": 32,  "hardware": "CPU: AMD Ryzen 7 7800X3D 8-Core Processor, RAM: 15.62 GB, CUDA: | NVIDIA-SMI 580.102.01 Driver Version: 581.57 CUDA Version: 13.0|",  "execution_time": "inference: 34.68s, metrics: 45.76ms",  "num_classes": 28}
    card_id = admin_card_id
    # 2. run import metrics
    response = client.post(f"/transparency/eval_adapter/{card_id}", json=metrics, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    text = json.loads(response.text)
    assert text['data'][4]['value'][1]['name'] == 'metrics'
    assert text['data'][4]['value'][1]['value']
    
def test_get_assistants(client, admin_token):
    response = client.get('/transparency/assistants', headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    