import json, requests, io
from pathlib import Path
from aicard.utils.image_converters import to_base64, to_bytes
from aicard.service.users import _ensure_db_integrity
from aicard.service.logger import Logger
from aicard.service.jobs_tracker import CardJobsTracker, Job
from aicard.agents.extensions.speedups import text_compression
from aicard.agents.extensions.embeddings import ImageClassifier
from aicard.utils.pdf_split import pdf_to_chunks
from codecarbon import EmissionsTracker
def test_admin_dashboard(client, admin_token):
    request = client.get('transparency/users', headers={"Authorization": f"Bearer {admin_token}"})
    assert request.status_code == 200
    
def test_image_coverters():
    path = 'ui/transparency/img/create_img.png'
    base64, status_code = to_base64(path)
    assert status_code == 200
    bytes, status_code = to_bytes(base64)
    assert status_code == 200
    bytes, status_code = to_bytes(path)
    assert status_code == 200
    base64, status_code = to_base64('')
    assert status_code == 500
    bytes, status_code = to_bytes('')
    assert status_code == 500
    
    
def test_ensure_db_integrity():
    logger = Logger()
    _ensure_db_integrity('db_pytest/auth.db', logger)
    # function has no return status
    
def test_CardJobsTracker():
    job_tracker = CardJobsTracker()
    job = Job()
    tracker = EmissionsTracker( project_name='test_job', save_to_file=False, log_level="WARNING", tracking_mode="process")
    tracker.start()
    assert job_tracker.set('test_job', job)
    assert job_tracker.update('test_job', job)
    assert job_tracker.get('test_job')
    emissions = tracker.stop()
    emissions_data = json.loads(tracker.final_emissions_data.toJSON())
    assert job_tracker.delete('test_job', emissions_data)
    assert bool(job_tracker.estimate_codecarbon('test_job'))

def test_text_compression():
    text = 'testing text compression'
    assert text_compression(text) != ''
    # there is no status return
    
def test_ImageClassifier():
    path = 'ui/transparency/img/create_img.png'
    img_classifier = ImageClassifier()
    assert not(img_classifier.classify_images([path])[0][0] is None)
    
def test_pdf_to_chunks():
    path = 'tests/data/2402.19091v2.pdf'
    assert bool(pdf_to_chunks(pdf_path=path))
    assert bool(pdf_to_chunks(pdf_path=path, char_per_chunk=1000))