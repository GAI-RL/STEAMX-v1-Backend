import urllib.request
import urllib.error

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/auth/google',
    data=b'{"token": "dummy"}',
    headers={'Content-Type': 'application/json'}
)

try:
    response = urllib.request.urlopen(req)
    print("Success:", response.read())
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.read())
except Exception as e:
    print("Exception:", e)
