import requests
try:
    files = {'file': open('uploads/sample_input.csv','rb')}
    resp = requests.post('http://127.0.0.1:5000/analyze', files=files, data={'industry':'retail'}, timeout=10)
    print('status', resp.status_code)
    print('text', resp.text[:1000])
except Exception as e:
    print('error', e)
