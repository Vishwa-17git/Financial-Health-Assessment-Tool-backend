import os, sys
# ensure backend package root is importable when tests run from workspace root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import io
import json
from app import app


def test_analyze_endpoint_csv(tmp_path):
    client = app.test_client()

    # Use the included sample_input.csv
    sample = open('uploads/sample_input.csv', 'rb')

    data = {
        'file': (sample, 'sample_input.csv'),
        'industry': 'retail'
    }

    resp = client.post('/analyze', content_type='multipart/form-data', data=data)
    assert resp.status_code == 200
    body = json.loads(resp.data)
    assert 'metrics' in body
    assert 'health_score' in body
    sample.close()
